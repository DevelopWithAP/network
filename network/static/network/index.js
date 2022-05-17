/**
 * Prevents content of length 0 or spaces from being submitted
 */

document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    const submitBtn = document.getElementById('submit');

    submitBtn.setAttribute('disabled', '');
    content.oninput = () => {
        if(content.value.trim().length == 0) {
            submitBtn.setAttribute('disabled', '');
        } else {
            submitBtn.removeAttribute('disabled');
        }
    };    
});