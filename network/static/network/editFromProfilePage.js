/**
 * Script to edit a post from the profile page asynchronously
 */

 document.addEventListener('DOMContentLoaded', () => {
    const editBtns = document.querySelectorAll('.edit');

    editBtns.forEach((btn) => {
        btn.onclick = () => {
            const postId = btn.dataset.postId;
            const userId = btn.dataset.userId;
            const currentContent = document.querySelector(`#content-${postId}`);
            const parentDiv = currentContent.parentElement;
            const editDiv = document.querySelector(`[data-edit-id="${postId}"]`);
            const updateArea = document.querySelector(`#update-content-${postId}`);
            updateArea.textContent = currentContent.textContent;

            parentDiv.style.display = 'none';
            editDiv.style.display = 'block';

            const saveUpdateBtn = document.querySelector(`[data-save-edit-id="${postId}"]`);
            const closeUpdateBtn = document.querySelector(`[data-close-edit-id="${postId}"]`);

            closeUpdateBtn.addEventListener('click', () => {
                parentDiv.style.display = 'block';
                editDiv.style.display = 'none';
            });

            saveUpdateBtn.addEventListener('click', () => {
                const updatedContent = updateArea.value;

                fetch(`/${userId}/edit/${postId}`, {
                    method: 'PUT',
                    body: JSON.stringify({ content: updatedContent })
                })
                    .then((response) => response.json())
                    .then((data) => {
                        currentContent.innerText = data.content;

                        editDiv.style.display = 'none';
                        parentDiv.style.display = 'block';
                    });

            });
        };

    });
});