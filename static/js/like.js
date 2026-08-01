// likes.js — dipakai di semua halaman yang render tombol like
import { getToken } from '/static/js/auth.js';

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.like-btn');
  if (!btn) return;

  const postId = btn.dataset.postId;
  const countEl = btn.parentElement.querySelector('.like-count');

  btn.classList.add('pop');
  setTimeout(() => btn.classList.remove('pop'), 350);
  btn.disabled = true;

  try {
    const token = getToken();
    if (!token) {
      alert('Silakan login dulu untuk like postingan ini.');
      btn.disabled = false;
      return;
    }

    const res = await fetch(`/api/posts/${postId}/likes`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      if (res.status === 401) alert('Silakan login dulu untuk like postingan ini.');
      else console.error('Gagal like post:', res.status);
      btn.disabled = false;
      return;
    }

    const data = await res.json();
    const isLiked = data.status === 'liked';
    
    btn.classList.toggle('liked', isLiked);
    btn.setAttribute('aria-pressed', isLiked);
    
    // Update count: increment if liked, decrement if unliked
    const currentCount = parseInt(countEl.textContent) || 0;
    countEl.textContent = isLiked ? currentCount + 1 : Math.max(0, currentCount - 1);
  } catch (err) {
    console.error('Error saat toggle like:', err);
  } finally {
    btn.disabled = false;
  }
});
