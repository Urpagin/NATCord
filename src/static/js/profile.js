import { setGlobalUser } from './globals.js';

// Utility function: Converts a File object to a Base64 string.
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

// Compress an image file using a canvas and JPEG encoding.
// quality: starting quality factor (0 to 1)
function compressImage(file, maxSize = 256 * 1024, quality = 0.7) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = function () {
            // Create a canvas with the same dimensions as the image.
            const canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);

            // Try to encode the canvas as a JPEG at the given quality.
            let dataUrl = canvas.toDataURL('image/jpeg', quality);
            // Estimate the size: the Base64 length times 3/4 (since 4 characters represent 3 bytes).
            const base64String = dataUrl.split(',')[1];
            const sizeInBytes = (base64String.length * 3) / 4;

            if (sizeInBytes > maxSize && quality > 0.1) {
                // If still too large, reduce quality and try again.
                compressImage(file, maxSize, quality - 0.1)
                    .then(resolve)
                    .catch(reject);
            } else {
                resolve(dataUrl);
            }
        };
        img.onerror = reject;
        // Read the file as a Data URL to set as the image source.
        const reader = new FileReader();
        reader.onload = function (e) {
            img.src = e.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Process the icon file: if its raw size is over 256KB, compress it; otherwise, use it directly.
async function processIconFile(file) {
    const MAX_SIZE = 256 * 1024; // 256 KB
    if (file.size <= MAX_SIZE) {
        return fileToBase64(file);
    } else {
        return compressImage(file, MAX_SIZE);
    }
}



document.getElementById("profileForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const iconInput = document.getElementById("icon");
    if (iconInput.files && iconInput.files[0]) {
        try {
            // Process the file, compressing it if needed.
            const processedBase64 = await processIconFile(iconInput.files[0]);
            document.getElementById("icon_b64").value = processedBase64;
        } catch (error) {
            console.error("Error processing icon file:", error);
        }
    }

    const formData = new FormData(this);
    const newUsername = formData.get("username");

    try {
        const response = await fetch("/profile", {
            method: "POST",
            body: formData
        });
        if (response.ok) {
            const updatedUser = await response.json();
            await setGlobalUser(updatedUser.username);
            alert("Profile updated successfully!");
            window.location.reload();
        }
        else {
            // Read the error message from the response and display it.
            const errorMsg = await response.json();
            alert("Error updating profile: " + errorMsg.error);
        }
    } catch (err) {
        console.error("Error submitting form:", err);
        alert("Error updating profile.");
    }
});


