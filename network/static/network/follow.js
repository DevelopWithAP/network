document.addEventListener('DOMContentLoaded', () => {

    const followBtn = document.querySelector('#follow-btn');

    followBtn.addEventListener('click', () => {
        const followers = document.querySelector('#followers');
        const userId = parseInt(followBtn.dataset.userId);
        const followerId = parseInt(followBtn.dataset.followerId);
        const action = followBtn.textContent.trim();

        const form = new FormData();
        form.append('user_id', userId);
        form.append('follower_id', followerId);
        form.append('action', action);

        fetch(`/follow/`, {
            method: 'POST',
            body: form
        })
            .then((response) => response.json())
            .then((result) => {
                followBtn.innerText = result.action;
                followers.innerText = result.followers;
            });
    });

});