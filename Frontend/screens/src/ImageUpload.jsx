import React, { useState } from 'react';
import porin_now from './assets/porin_wait.png'; 
import right_img from './assets/Left-Place-Holder.jpg'; 
import './ImageUpload.css';

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImage(URL.createObjectURL(file));
      setError('');
    } else {
      setError('Please upload a valid image file.');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setImage(URL.createObjectURL(file));
      setError('');
    } else {
      setError('Please upload a valid image file.');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleUpload = () => {
    if (image) {
      const formData = new FormData();
      formData.append('file', image);
  
      fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.file_id) {
            alert(`Image uploaded successfully! File ID: ${data.file_id}`);
          } else {
            alert(`Upload failed: ${data.error}`);
          }
        })
        .catch((error) => {
          console.error('Error uploading image:', error);
        });
    } else {
      setError('Please select an image to upload.');
    }
  };
  

  return (
    <div className="page-container">
      <div className="heady">
      <header>
        <h1>META CLOSET</h1>
        <p>Your virtual wardrobe</p>
      </header>
      </div>
       {/* <div className='shadow'> .</div> */}
      <section className="about-section">
  {/* <h2>About Meta Closet</h2>
  <div className="about-content-container">
    <p className="mini-about">
      Meta Closet helps you try outfits virtually and organize your wardrobe effortlessly.
      Upload an image of your outfit, and we'll help you style it with our virtual wardrobe.
      Whether you're looking for casual wear, formal attire, or something in between, Meta Closet has got you covered.
      Our advanced AI suggests outfit combinations based on your preferences, trends, and occasions. You can also mix and match clothing
      items, explore new fashion styles, and keep track of your favorite looks. Stay organized with personalized recommendations and seasonal
      outfit planners. With Meta Closet, your perfect outfit is always just a click away! Plus, share your looks with friends,
      get real-time feedback, and stay ahead with the latest fashion updates and style inspirations.
    </p>
    <img
      src={right_img}
      alt="About Meta Closet"
      className="about-description-image"
    />
  </div>
  <br /> */}
  <br />
  <div className="upload-instruction-container">
    <p className="upload-instruction">Upload an image to get started!</p>
    <img
      src={porin_now}
      alt="Lubieee__"
      className="moving-image"
    />
  </div>
</section>

      
      <section className="upload-section">
        <div className="upload-container">
          <div className="drop-zone" onDrop={handleDrop} onDragOver={handleDragOver}>
            {image ? (
              <img src={image} alt="Uploaded" className="uploaded-image" />
            ) : (
              <div className="upload-text">
                <p>Drag & Drop an image here or click to upload</p>
              </div>
            )}
          </div>
          <br />
          <div className="button-container">
            <input
              type="file"
              id="file-input"
              accept="image/*"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-input" className="choose-button">
              Choose Image
            </label>
            <button className="upload-button" onClick={handleUpload}>
              Upload Image
            </button>
          </div>
          {error && <p className="error-message">{error}</p>}
        </div>
      </section>

      {/* <section className="image-scroll">
        <div className="image-row">
          <img src="dress1.png" alt="Outfit 1" />
          <img src="dress2.png" alt="Outfit 2" />
          <img src="dress3.png" alt="Outfit 3" />
          <img src="dress4.png" alt="Outfit 4" />
          <img src="dress5.png" alt="Outfit 5" />
          <img src="dress1.png" alt="Outfit 1" />
          <img src="dress2.png" alt="Outfit 2" />
          <img src="dress3.png" alt="Outfit 3" />
          <img src="dress4.png" alt="Outfit 4" />
          <img src="dress5.png" alt="Outfit 5" />
        </div>
      </section> */}

      {/* Footer Section */}
      <footer className="footer">
        <p>© 2025 Meta Closet. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default ImageUpload;