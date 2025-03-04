// Interactive Nutrition Percentage Calculator 
document.addEventListener('DOMContentLoaded', function() {
    const carbsInput = document.getElementById('carbs-input');
    const proteinInput = document.getElementById('protein-input');
    const fatInput = document.getElementById('fat-input');
    const totalPercentage = document.getElementById('total-percentage');
    
    updateSumDisplay(); 

    carbsInput.addEventListener('input', updateSumDisplay);
    proteinInput.addEventListener('input', updateSumDisplay);
    fatInput.addEventListener('input', updateSumDisplay);

    function updateSumDisplay() {
        const carbsValue = parseInt(carbsInput.value) || 0;
        const proteinValue = parseInt(proteinInput.value) || 0;
        const fatValue = parseInt(fatInput.value) || 0;

        const newSum = carbsValue + proteinValue + fatValue;
        totalPercentage.textContent = newSum + '%';
    }
});


// Stopwatch

let interval;
let started = false;
let hours = 0;
let minutes = 0;
let seconds = 0;

function toggleStopwatch() {
    let currentTime = new Date().getTime();

    if (started) {
        clearInterval(interval);
        document.getElementById('startStopBtn').innerText = 'Start fasting';
        localStorage.removeItem('stopwatchStarted');
        localStorage.removeItem('stopwatchStartTime');
        
        let message = generateFastingMessage();
        document.getElementById('fastingMessage').innerText = message;
    } else {
        interval = setInterval(updateStopwatch, 1000); 
        document.getElementById('startStopBtn').innerText = 'Stop fasting';
        localStorage.setItem('stopwatchStarted', true);
        localStorage.setItem('stopwatchStartTime', currentTime);

        // Hide the fasting message
        document.getElementById('fastingMessage').innerText = '';
    }
    started = !started;
}

function updateStopwatch() {
    let currentTime = new Date().getTime();
    let startTime = parseInt(localStorage.getItem('stopwatchStartTime'));
    let elapsedTime = currentTime - startTime;

    seconds = Math.floor((elapsedTime / 1000) % 60);
    minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
    hours = Math.floor((elapsedTime / (1000 * 60 * 60)) % 24);

    document.getElementById('hours').innerText = (hours < 10 ? '0' : '') + hours + ":";
    document.getElementById('minutes').innerText = (minutes < 10 ? '0' : '') + minutes + ":";
    document.getElementById('seconds').innerText = (seconds < 10 ? '0' : '') + seconds;
}

function resetStopwatch() {
    clearInterval(interval);
    started = false;
    hours = 0;
    minutes = 0;
    seconds = 0;

    document.getElementById('hours').innerText = '00';
    document.getElementById('minutes').innerText = '00';
    document.getElementById('seconds').innerText = '00';
    document.getElementById('startStopBtn').innerText = 'Start fasting';
    localStorage.removeItem('stopwatchStarted');
    localStorage.removeItem('stopwatchStartTime');
}

function restoreStopwatch() {
    let stopwatchStarted = localStorage.getItem('stopwatchStarted');
    let stopwatchStartTime = localStorage.getItem('stopwatchStartTime');

    if (stopwatchStarted && stopwatchStartTime) {
        let currentTime = new Date().getTime();
        let elapsedTime = currentTime - parseInt(stopwatchStartTime);

        seconds = Math.floor((elapsedTime / 1000) % 60);
        minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
        hours = Math.floor((elapsedTime / (1000 * 60 * 60)) % 24);

        started = true;
        interval = setInterval(updateStopwatch, 1000);
        document.getElementById('startStopBtn').innerText = 'Stop fasting';
    }
}

function generateFastingMessage() {
    if (hours > 0) {
        return `Congratulations! You have fasted for ${hours} hour${hours > 1 ? 's' : ''}, ${minutes} minute${minutes !== 1 ? 's' : ''}, and ${seconds} second${seconds !== 1 ? 's' : ''}.`;
    } else if (minutes > 0) {
        return `Congratulations! You have fasted for ${minutes} minute${minutes > 1 ? 's' : ''} and ${seconds} second${seconds !== 1 ? 's' : ''}.`;
    } else {
        return `Congratulations! You have fasted for ${seconds} second${seconds !== 1 ? 's' : ''}.`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    restoreStopwatch();
});



// Calendar
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('selected-date').addEventListener('change', function() {
    
        document.getElementById('date-form').submit();
    });
});


// Calculate values based on grams
document.addEventListener('DOMContentLoaded', function() {
    let gramsInput = document.getElementById('grams-input');
    let calorieValue = document.getElementById('calorie-value-template').value;
    let proteinValue = document.getElementById('protein-value-template').value;
    let carbsValue = document.getElementById('carbs-value-template').value;
    let fibersValue = document.getElementById('fibers-value-template').value;
    let sugarsValue = document.getElementById('sugars-value-template').value;
    let fatValue= document.getElementById('fat-value-template').value;
    let saturatedFatValue = document.getElementById('saturated-fat-value-template').value;
    let sodiumValue= document.getElementById('sodium-value-template').value;
    

    gramsInput.addEventListener('input', function() {
        // Get the new grams value
        let grams = parseFloat(this.value);
        if (grams && grams !== 100) {  


        // Calculate new nutrition values
        let nutritionValues = calculateNutritionValues(grams, calorieValue, proteinValue, carbsValue, fibersValue, sugarsValue, fatValue, saturatedFatValue, sodiumValue);

        // Update the DOM elements with the new values
        document.getElementById('calories-value').textContent = nutritionValues.calories;
        document.getElementById('protein-value').textContent = nutritionValues.protein;
        document.getElementById('carbs-value').textContent = nutritionValues.carbs;
        document.getElementById('fibers-value').textContent = nutritionValues.fibers;
        document.getElementById('sugar-value').textContent = nutritionValues.sugar;
        document.getElementById('fat-value').textContent = nutritionValues.fat;
        document.getElementById('saturated-fat-value').textContent = nutritionValues.saturatedFat;
        document.getElementById('sodium-value').textContent = nutritionValues.sodium;
        document.getElementById('updated-calorie').value = nutritionValues.calories;
        document.getElementById('updated-total_protein').value = nutritionValues.protein;
        document.getElementById('updated-total_carbs').value = nutritionValues.carbs;
        document.getElementById('updated-dietary_fibers').value = nutritionValues.fibers;
        document.getElementById('updated-sugars').value = nutritionValues.sugar;
        document.getElementById('updated-total_fat').value = nutritionValues.fat;
        document.getElementById('updated-saturated_fat').value = nutritionValues.saturatedFat;
        document.getElementById('updated-sodium').value = nutritionValues.sodium;
        document.getElementById('updated-grams').value = grams;
        }

    });

});

function calculateNutritionValues(grams, calorieValue, proteinValue, carbsValue, fibersValue, sugarsValue, fatValue, saturatedFatValue, sodiumValue) {

    return {
        calories: (parseFloat(calorieValue) / 100 * grams).toFixed(1), 
        protein: (parseFloat(proteinValue) / 100 * grams).toFixed(1), 
        carbs: (parseFloat(carbsValue) / 100 * grams).toFixed(1), 
        fibers: (parseFloat(fibersValue) / 100 * grams).toFixed(1),
        sugar: (parseFloat(sugarsValue) / 100 * grams).toFixed(1), 
        fat: (parseFloat(fatValue) / 100 * grams).toFixed(1), 
        saturatedFat: (parseFloat(saturatedFatValue) / 100 * grams).toFixed(1), 
        sodium: (parseFloat(sodiumValue) / 100 * grams).toFixed(1),
    };
}

// Read more/read less

function readMore(cardId) {
    let moreText = document.getElementById("more-" + cardId);
    let btnText = document.getElementById("myBtn-" + cardId);
  
    if (moreText.style.display === "none") {
      btnText.innerHTML = "Read Less"; 
      moreText.style.display = "inline";
    } else {
      btnText.innerHTML = "Read More"; 
      moreText.style.display = "none";
    }
  }


function toggleInstructions(id) {
    let instructions = document.getElementById('instructions-' + id);
    let link = instructions.nextElementSibling; 
  
    if (instructions.style.display === 'none') {
      instructions.style.display = 'block'; 
      link.innerHTML = 'Read Less'; 
    } else {
      instructions.style.display = 'none'; 
      link.innerHTML = 'Read More'; 
    }
  }


