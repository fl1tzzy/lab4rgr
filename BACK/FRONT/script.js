<script>
  console.log("script loaded");

  const loginForm = document.getElementById('login-form'),
        regForm   = document.getElementById('register-form');

  document.getElementById('show-login').onclick = () => {
    loginForm.classList.remove('hidden');
    regForm.classList.add('hidden');
  };
  document.getElementById('show-register').onclick = () => {
    regForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
  };

  // Регистрация
  document.getElementById('btn-register').onclick = async () => {
    const email    = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const res = await fetch('https://127.0.0.1:8000/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    alert(res.ok ? 'Регистрация успешна' : 'Ошибка регистрации');
  };

  // Вход
  document.getElementById('btn-login').onclick = async () => {
    const email    = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const res = await fetch('https://127.0.0.1:8000/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      alert('Ошибка входа');
      return;
    }
    const { access_token } = await res.json();
    localStorage.setItem('jwt_token', access_token);
    console.log('JWT Token:', access_token);
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('appointment-section').classList.remove('hidden');
  };

  // Показ формы записи
  document.getElementById('open-form-btn').onclick = () => {
    document.getElementById('appointment-form').classList.remove('hidden');
  };

  // Поиск врачей
  document.getElementById('find-doctors-btn').onclick = async () => {
    const symptoms = document.getElementById('symptoms').value
      .split(',').map(s => s.trim());
    const res = await fetch('https://127.0.0.1:8000/doctors-by-symptoms/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('jwt_token')
      },
      body: JSON.stringify({ symptoms })
    });
    if (!res.ok) {
      alert('Ошибка получения врачей');
      return;
    }
    const docs = await res.json();
    const sel = document.getElementById('doctor');
    sel.innerHTML = '<option value="">--выберите врача--</option>';
    docs.forEach(d => {
      const o = document.createElement('option');
      o.value = d.id;
      o.textContent = `${d.name} (${d.specialization})`;
      o.dataset.schedule = d.schedule;
      sel.appendChild(o);
    });
  };

  // Заполнение времени
  document.getElementById('doctor').onchange = () => {
    const sched = document.getElementById('doctor')
      .selectedOptions[0]?.dataset.schedule || '';
    const times = sched.split(',');
    const timeSel = document.getElementById('appointment-time');
    timeSel.innerHTML = '<option value="">--выберите время--</option>';
    times.forEach(t => {
      const o = document.createElement('option');
      o.value = t; o.textContent = t;
      timeSel.appendChild(o);
    });
  };

  // Отправка записи
  document.getElementById('submit-appointment-btn').onclick = async () => {
    const doctor_id       = +document.getElementById('doctor').value;
    const appointment_time = document.getElementById('appointment-time').value;
    const symptoms        = document.getElementById('symptoms').value;
    const res = await fetch('https://127.0.0.1:8000/appointments/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('jwt_token')
      },
      body: JSON.stringify({ doctor_id, user_id: 1, symptoms, appointment_time })
    });
    alert(res.ok ? 'Запись создана' : 'Ошибка создания записи');
  };
</script>
