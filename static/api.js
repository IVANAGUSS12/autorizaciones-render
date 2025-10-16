// static/panel/api.js

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

async function apiGet(url) {
  const res = await fetch(url, {
    method: 'GET',
    credentials: 'include',          // << manda cookie de sesión
    headers: { 'Accept': 'application/json' }
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

async function apiPost(url, body, needsCsrf=false) {
  const headers = {};
  if (needsCsrf) headers['X-CSRFToken'] = getCookie('csrftoken');

  const res = await fetch(url, {
    method: 'POST',
    credentials: 'include',          // << manda cookie de sesión
    headers,
    body                              // FormData o JSON.stringify(...)
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

// ---- ejemplos para usar en el panel ----
window.fetchPatients = (params = {}) => {
  const qs = new URLSearchParams(params).toString();
  return apiGet(`/v1/patients/${qs ? '?' + qs : ''}`);
};

window.createAttachment = (formData) => {
  // create de Attachment está exento de CSRF en backend
  return apiPost('/v1/attachments/', formData, /*needsCsrf=*/false);
};
