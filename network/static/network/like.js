/**
 * Imlements the 'Like/Unlike' functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    const likeSpans = document.querySelectorAll('.like');

    likeSpans.forEach((likeSpan) => {
        likeSpan.onclick = () => {
            const postId = likeSpan.children[0].dataset.id;
            const action = likeSpan.children[0].dataset.action;

            likeIcon = document.querySelector(`[data-id="${postId}"]`);
            likesField = document.querySelector(`#likes-count-${postId}`);
            fetch(`like/${postId}`, {
                method: 'POST',
                body: JSON.stringify({
                    post_id: postId,
                    action: action
                })
            })
                .then((response) => response.json())
                .then((result) => {
                    if (result.action == 'like') {
                        likesField.textContent = result.likes;
                        likeIcon.setAttribute('data-action', `${result.action}`);
                        likeIcon.classList.replace('fas', 'far');
                    } else if (result.action == 'unlike') {
                        likesField.textContent = result.likes;
                        likeIcon.setAttribute('data-action', `${result.action}`);
                        likeIcon.classList.replace('far', 'fas');
                    }
                    
                });
        };
    });

});