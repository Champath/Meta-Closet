import React, { useEffect, useState } from 'react';
import ImageUpload from './ImageUpload';
import './LubiePage.css';
import lubieImage from './assets/excited_lubie.png';

const LubiePage = () => {
  const [showFilePage, setShowFilePage] = useState(false);
  const [lubieVisible, setLubieVisible] = useState(false);
  const [metaClosetVisible, setMetaClosetVisible] = useState(false);
  const [zoomLubie, setZoomLubie] = useState(false); // State to control Lubie's zoom animation

  useEffect(() => {
    const metaClosetTimer = setTimeout(() => {
      setMetaClosetVisible(true);
    }, 500);

    const lubieTimer = setTimeout(() => {
      setLubieVisible(true);
    }, 2000);

    return () => {
      clearTimeout(metaClosetTimer);
      clearTimeout(lubieTimer);
    };
  }, []);

  const handleStart = () => {
    setZoomLubie(true);

    setTimeout(() => {
      setShowFilePage(true);
    }, 1000); // Match the zoom animation duration
  };

  return (
    <div className="lubie-page">
      {!showFilePage ? (
        <>
          {metaClosetVisible && (
            <div className="meta-closet-text headie">Meta Closet</div>
          )}
          {lubieVisible && (
            <div className={`lubie-container ${zoomLubie ? 'zoom' : ''}`}>
              <div className="lubie-dialog">
                <img
                  src={lubieImage}
                  alt="Lubie the Poring"
                  className="lubie-image"
                />
                <p>Hey, I am Lubie! Let's start!</p>
                <button onClick={handleStart}>OK</button>
              </div>
            </div>
          )}
        </>
      ) : (
        <ImageUpload />
      )}
    </div>
  );
};

export default LubiePage;
