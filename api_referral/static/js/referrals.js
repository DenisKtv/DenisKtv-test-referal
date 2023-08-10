function getReferrals() {
    var phone_number = prompt("Введите свой номер телефона:");
    if (phone_number) {
        fetch('{% url "referrals-list" %}?phone_number=' + phone_number)
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else {
                var referralListDiv = document.querySelector('#referral-list');
                referralListDiv.innerHTML = '';
                data.forEach(referral => {
                    var referralDiv = document.createElement('div');
                    referralDiv.textContent = "Телефон: " + referral.phone_number + ", Инвайт-код: " + referral.invite_code;
                    referralListDiv.appendChild(referralDiv);
                });
            }
        })
        .catch(error => {
            console.error('Произошла ошибка при выполнении запроса:', error);
            alert('Произошла ошибка при выполнении запроса');
        });
    }
}
