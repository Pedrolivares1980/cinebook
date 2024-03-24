document.addEventListener("DOMContentLoaded", function() {
    // Handle like button clicks for posts
    const postLikeButtons = document.querySelectorAll('.like-post');
    postLikeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.dataset.id;
            fetch('/blog/like_post/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ id: postId }),
            })
            .then(response => response.json())
            .then(data => {
                const likeCountSpan = document.getElementById(`like-count-post-${postId}`);
                const likeButton = document.getElementById(`like-btn-post-${postId}`);
                likeCountSpan.innerText = `${data.total_likes} likes`;
                updateLikeButton(likeButton, data.liked);
            });
        });
    });

    // Handle like button clicks for comments
    const commentLikeButtons = document.querySelectorAll('.like-comment');
    commentLikeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const commentId = this.dataset.id;
            fetch('/blog/like_comment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ id: commentId }),
            })
            .then(response => response.json())
            .then(data => {
                const likeCountSpan = document.getElementById(`like-count-comment-${commentId}`);
                const likeButton = document.getElementById(`like-btn-comment-${commentId}`);
                likeCountSpan.innerText = `${data.total_likes} likes`;
                updateLikeButton(likeButton, data.liked);
            });
        });
    });

    // Function to update the like button's text and class based on the like status
    function updateLikeButton(button, isLiked) {
        if (isLiked) {
            button.innerText = 'Unlike';
            button.classList.remove('btn-primary');
            button.classList.add('btn-danger');
        } else {
            button.innerText = 'Like';
            button.classList.remove('btn-danger');
            button.classList.add('btn-primary');
        }
    }

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
