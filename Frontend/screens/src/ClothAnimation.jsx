import React, { useEffect, useRef, useState } from 'react';
import './ClothAnimation.css';
import leftDoorImage from './assets/curtain.png';
import rightDoorImage from './assets/curtain.png';
import LubiePage from './Lubie';

const ClothAnimation = () => {
  const leftDoorRef = useRef(null);
  const rightDoorRef = useRef(null);
  const [showAnimation, setShowAnimation] = useState(false);

  useEffect(() => {
  
    const lastShown = localStorage.getItem('lastAnimationShown');
    const now = new Date().getTime();
    const oneMonthInMillis = (30*24*60*60* 1000).toString(); // 30 days in milliseconds
   
    console.log('Last shown:', lastShown);
    console.log('Current time:', now);

    // if (!lastShown || now - parseInt(lastShown) > oneMonthInMillis) {
    //   console.log('Showing animation...');
     setShowAnimation(true);
    //   localStorage.setItem('lastAnimationShown', now.toString()); // Save the current timestamp
    // } else {
    //   console.log('Skipping animation...');
    //   setShowAnimation(false);
    //}
  }, []);

  useEffect(() => {
    if (showAnimation && leftDoorRef.current && rightDoorRef.current) {
      const timer = setTimeout(() => {
        console.log('Starting door animations...');
        leftDoorRef.current.classList.add('animate-left-door');
        rightDoorRef.current.classList.add('animate-right-door');
      }, 100);

      return () => clearTimeout(timer);
    }
  }, [showAnimation]);

  return (
    <div className="cloth-container">
      {showAnimation && (
        <>
          {}
          <div
            ref={leftDoorRef}
            className="door left-door"
            style={{ backgroundImage: `url(${leftDoorImage})` }}
          ></div>
          <div
            ref={rightDoorRef}
            className="door right-door"
            style={{ backgroundImage: `url(${rightDoorImage})` }}
          ></div>
        </>
      )}

      <div className="content">
        <LubiePage />
      </div>
    </div>
  );
};

export default ClothAnimation;