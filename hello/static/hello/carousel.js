var i = 1;

const ElList = document.querySelectorAll('.carousel__body__el');
const numOfEl = ElList.length;


// carousel built by me
const carouselright = () => {
    if (i < numOfEl) {
        i += 1;
        for(var l=1;l<=numOfEl;l++){
            if(l !== i) {
              document.querySelector(`.carousel__body-${l}`).classList.remove('body-active');  
              document.querySelector(`.h1-${l}`).classList.remove('h1-active');
              document.querySelector(`.p-${l}`).classList.remove('p-active');
            }
        }

        document.querySelector(`.carousel__body-${i}`).classList.add('body-active');  
        document.querySelector(`.h1-${i}`).classList.add('h1-active');
        document.querySelector(`.p-${i}`).classList.add('p-active');
    } else if(i >= numOfEl){
        i = 1;
        for(var l=2;l<=numOfEl;l++){
              document.querySelector(`.carousel__body-${l}`).classList.remove('body-active');  
              document.querySelector(`.h1-${l}`).classList.remove('h1-active');
              document.querySelector(`.p-${l}`).classList.remove('p-active'); 
        }

        document.querySelector(`.carousel__body-1`).classList.add('body-active'); 
        document.querySelector(`.h1-1`).classList.add('h1-active');
        document.querySelector(`.p-1`).classList.add('p-active');
    } 
}

const carouselleft = () => {
    if (i > 1) {
        i -=1;
        for(var l=1;l<=numOfEl;l++){
            if(l !== i) {
    
              document.querySelector(`.carousel__body-${l}`).classList.remove('body-active');  
              document.querySelector(`.h1-${l}`).classList.remove('h1-active');
              document.querySelector(`.p-${l}`).classList.remove('p-active');  
            }
        }

        document.querySelector(`.carousel__body-${i}`).classList.add('body-active');
        document.querySelector(`.h1-${i}`).classList.add('h1-active');
        document.querySelector(`.p-${i}`).classList.add('p-active');
    } else if(i <= 1) {
        i = numOfEl;
        for(var l=1;l<=numOfEl;l++){
            if(l !== i) {
  
              document.querySelector(`.carousel__body-${l}`).classList.remove('body-active');  
              document.querySelector(`.h1-${l}`).classList.remove('h1-active');
              document.querySelector(`.p-${l}`).classList.remove('p-active');   
            }
        }

        document.querySelector(`.carousel__body-${i}`).classList.add('body-active');
        document.querySelector(`.h1-${i}`).classList.add('h1-active');
        document.querySelector(`.p-${i}`).classList.add('p-active');
    }
}

//CAROUSEL
// when clicking carousel right button
document.querySelector('.carousel__right').addEventListener('click',carouselright);
// when clicking carousel left button
document.querySelector('.carousel__left').addEventListener('click',carouselleft);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function waitCar () {
      await sleep(5000);
      carouselright();
      waitCar();
};

// auto go to right after 5 second
waitCar();


document.onkeydown = function(event) {
    if (event.keyCode === 39) {
    event.preventDefault();
    document.querySelector(".carousel__right").click();
  } else if (event.keyCode === 37) {
    event.preventDefault();
    document.querySelector(".carousel__left").click();
  }
}
