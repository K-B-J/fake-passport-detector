let opacity = 0
let intervalID = 0
const temp = () => {
    setInterval(hide, 200)
}
const hide = () => {
    let message = document.getElementById("message")
    opacity =
        Number(window.getComputedStyle(message).getPropertyValue("opacity"))

    if (opacity > 0) {
        opacity = opacity - 0.1
        message.style.opacity = opacity
    }
    else {
        clearInterval(intervalID)
    }
}
const display = () => {
    let message = document.getElementById("message")
    message.style.display = "none"
}
const fadeout = () => {
    setTimeout(temp, 12000)
    setTimeout(display, 14000)
}
window.onload = fadeout
