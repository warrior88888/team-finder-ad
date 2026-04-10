// Favorites add and remove
(function() {
    "use strict";

    const getCsrfToken = () => {
        return document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1] ||
            document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    };

    async function toggleFavorite(button) {
        if (button.disabled) return;

        const { projectId, fav } = button.dataset;
        const isCurrentlyFav = fav === "true";
        const isFavoritesPage = document.body.dataset.page === "favorites";

        button.disabled = true;

        try {
            const response = await fetch(`/projects/${projectId}/toggle-favorite/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCsrfToken()
                },
                body: JSON.stringify({})
            });

            if (!response.ok) throw new Error('Network response was not ok');

            if (isFavoritesPage && isCurrentlyFav) {
                const card = button.closest(".project-card");
                card.style.transition = "all 0.2s ease";
                card.style.opacity = "0";
                card.style.transform = "scale(0.95)";

                setTimeout(() => {
                    card.remove();
                    if (document.querySelectorAll(".project-card").length === 0) {
                        const emptyBlock = document.querySelector("#empty-favorite-template");
                        if (emptyBlock) emptyBlock.style.display = "block";
                        else location.reload();
                    }
                }, 200);
            } else {
                const newState = !isCurrentlyFav;
                button.dataset.fav = String(newState);
                button.classList.toggle("favorite", newState);
                button.classList.toggle("not-favorite", !newState);
            }

        } catch (error) {
            console.error("Favorite Error:", error);
        } finally {
            button.disabled = false;
        }
    }

    document.addEventListener("click", (e) => {
        const favBtn = e.target.closest(".project-fav-icon");
        if (favBtn) {
            e.preventDefault();
            toggleFavorite(favBtn);
        }
    });

})();
