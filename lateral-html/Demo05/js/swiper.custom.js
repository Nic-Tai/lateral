/*------------------------------------------------------------------
Initialize Swiper
-------------------------------------------------------------------*/
"use strict";
var swipert = new Swiper ('.hiw-titles', {
spaceBetween: 1,
centeredSlides: true,
slidesPerView: 'auto',
touchRatio: 1,
slideToClickedSlide: true
}); 
var swiperc = new Swiper ('.hiw-content', {
direction: 'horizontal',
effect: 'slide'
}); 

swipert.controller.control = swiperc;
swiperc.controller.control = swipert;
