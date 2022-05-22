/**
 * Handles the deletion of a post
 */

document.addEventListener('DOMContentLoaded', () => {
    const deleteBtns = document.querySelectorAll('.delete');

    deleteBtns.forEach((btn) => {
        const postId = btn.dataset.deleteId;
        const action = btn.dataset.action

        btn.onclick = () => {
            fetch(`toggle_visibility/${postId}`, {
                method: 'POST',
                body: JSON.stringify({
                    post_id: postId,
                    action: action
                })
            })
                .then((response) => response.json())
                .then((result) => {
                    console.log(result);
                    location.reload();
                });
        };
    });

});