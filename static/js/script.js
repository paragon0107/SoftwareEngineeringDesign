//
// function openLoginModal() {
//     document.getElementById('loginModal').style.display = 'block';
// }
//
// function closeLoginModal() {
//     document.getElementById('loginModal').style.display = 'none';
// }
//
// function login() {
//     var username = document.getElementById('username').value;
//     var password = document.getElementById('password').value;
//
//     if (username === 'user' && password === 'password') {
//         alert('Login successful!');
//         closeLoginModal();
//     } else {
//         alert('Invalid username or password.');
//     }
// }
//
// window.onclick = function(event) {
//     var modal = document.getElementById('loginModal');
//     if (event.target === modal) {
//         modal.style.display = 'none';
//     }
// }
//
// // function login(event) {
// //     event.preventDefault();
// //     var username = document.getElementById('signinUsername').value;
// //     var password = document.getElementById('signinPassword').value;
// //
// //     if (username === 'user' && password === 'password') {
// //         alert('Login successful!');
// //         window.location.href = 'myprofile.html';
// //     } else {
// //         alert('Invalid username or password.');
// //     }
// // }
//
// document.getElementById('uploadForm')?.addEventListener('submit', function(event) {
//     event.preventDefault();
//     var photoUpload = document.getElementById('photoUpload').files[0];
//     var photoDescription = document.getElementById('photoDescription').value;
//     var photoKeywords = document.getElementById('photoKeywords').value;
//
//     var photoContainer = document.createElement('div');
//     var photo = document.createElement('img');
//     var description = document.createElement('p');
//     var keywords = document.createElement('p');
//
//     var reader = new FileReader();
//     reader.onload = function(e) {
//         photo.src = e.target.result;
//     };
//     reader.readAsDataURL(photoUpload);
//
//     description.textContent = "Description: " + photoDescription;
//     keywords.textContent = "Keywords: " + photoKeywords;
//
//     photoContainer.appendChild(photo);
//     photoContainer.appendChild(description);
//     photoContainer.appendChild(keywords);
//
//     document.getElementById('uploadedPhotos').appendChild(photoContainer);
// });
//
// let photos = [];
//
// // Simulated photo data
// photos = [
//     {
//         src: 'path/to/photo1.jpg',
//         description: 'Beautiful sunrise',
//         keywords: 'sunrise, nature'
//     },
//     {
//         src: 'path/to/photo2.jpg',
//         description: 'City skyline',
//         keywords: 'city, skyline'
//     }
//     // Add more photos here
// ];
//
// function loadFeed() {
//     const photoFeed = document.getElementById('photoFeed');
//     photoFeed.innerHTML = '';
//
//     photos.forEach(photo => {
//         const photoItem = document.createElement('div');
//         photoItem.className = 'photo-item';
//
//         const img = document.createElement('img');
//         img.src = photo.src;
//
//         const description = document.createElement('p');
//         description.textContent = photo.description;
//
//         const keywords = document.createElement('p');
//         keywords.textContent = `Keywords: ${photo.keywords}`;
//
//         photoItem.appendChild(img);
//         photoItem.appendChild(description);
//         photoItem.appendChild(keywords);
//         photoFeed.appendChild(photoItem);
//     });
// }
//
// function searchPhotos() {
//     const input = document.getElementById('searchInput').value.toLowerCase();
//     const filteredPhotos = photos.filter(photo =>
//         photo.keywords.toLowerCase().includes(input) ||
//         photo.description.toLowerCase().includes(input)
//     );
//
//     const photoFeed = document.getElementById('photoFeed');
//     photoFeed.innerHTML = '';
//
//     filteredPhotos.forEach(photo => {
//         const photoItem = document.createElement('div');
//         photoItem.className = 'photo-item';
//
//         const img = document.createElement('img');
//         img.src = photo.src;
//
//         const description = document.createElement('p');
//         description.textContent = photo.description;
//
//         const keywords = document.createElement('p');
//         keywords.textContent = `Keywords: ${photo.keywords}`;
//
//         photoItem.appendChild(img);
//         photoItem.appendChild(description);
//         photoItem.appendChild(keywords);
//         photoFeed.appendChild(photoItem);
//     });
// }
//
// // Automatically load the feed on page load
// document.addEventListener('DOMContentLoaded', loadFeed);
//
