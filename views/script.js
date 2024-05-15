const CURRENT_EVENT = "http://127.0.0.1:5000/current_event"

async function get_current_event(){
    const response = await fetch(CURRENT_EVENT);
    const data = await response.json();
    
    return data
}

async function display_current_event(){
    const divElement = document.querySelector('.event')
    divElement.classList.remove('hidden')

    divElement.classList.add('display')
    data = await get_current_event()
    console.log(data)
    const eventNameElement = document.createElement('h2')
    const eventEffectElement = document.createElement('p')
    eventNameElement.textContent = data.desc
    if (data.amount > 0){
        eventEffectElement.textContent = `Vous gagnez ${data.amount} ${data.key} ! lets go !`
    }
    else{
        eventEffectElement.textContent = `Vous perdez ${data.amount} ${data.key} ! Chiant !`
    }
    
    divElement.appendChild(eventNameElement)
    divElement.appendChild(eventEffectElement)
    setTimeout(function() {
        divElement.classList.remove('display')
        divElement.classList.add('hidden')
    }, 5000);
    
}

display_current_event()
    

