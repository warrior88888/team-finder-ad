// Avatar management logic
(function() {
    const avatarInput = document.getElementById('id_avatar');
    const avatarImage = document.querySelector('.avatar-preview img');
    const clearBtn = document.getElementById('clear-avatar-btn');

    const initialSrc = avatarImage ? avatarImage.dataset.original : '';

    if (avatarInput && avatarImage) {
        avatarInput.addEventListener('change', function() {
            const file = this.files[0];

            if (file) {
                if (!file.type.startsWith('image/')) {
                    alert('Ошибка: Можно загружать только изображения (JPG, PNG, WEBP).');
                    this.value = '';
                    avatarImage.src = initialSrc;
                    return;
                }

                const maxSizeInMB = 5;
                if (file.size > maxSizeInMB * 1024 * 1024) {
                    alert(`Ошибка: Файл слишком тяжелый. Максимальный размер — ${maxSizeInMB} МБ.`);
                    this.value = '';
                    avatarImage.src = initialSrc;
                    return;
                }

                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarImage.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', async function() {
            const resetUrl = clearBtn.dataset.resetUrl;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch(resetUrl, {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrfToken},
                });

                if (response.status === 429) {
                    alert('Слишком много запросов. Попробуйте позже.');
                    return;
                }

                if (!response.ok) {
                    alert('Ошибка при сбросе аватара. Попробуйте ещё раз.');
                    return;
                }

                const data = await response.json();
                const avatarUrl = `${data.avatar_url}?v=${Date.now()}`;
                avatarImage.src = avatarUrl;
                avatarImage.dataset.original = avatarUrl;
                avatarInput.value = '';

            } catch (e) {
                alert('Ошибка сети. Попробуйте ещё раз.');
            }
        });
    }
})();