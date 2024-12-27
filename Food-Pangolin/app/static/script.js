function confirmOrder(orderId) {
    if (confirm("確定接單嗎？")) {
        // 跳轉到接單的路由
        window.location.href = `/accept_order?order_id=${orderId}`;
    }
}

function openRatingModal(orderId) {
    // 設定表單的訂單ID
    document.getElementById('modalOrderId').value = orderId;
    document.getElementById('ratingForm').action = `/rate_customer_and_complete/${orderId}`;
    document.getElementById('ratingModal').style.display = 'block';
}


function closeRatingModal() {
    // 隱藏模態框
    document.getElementById('ratingModal').style.display = 'none';
}

document.getElementById('ratingForm').onsubmit = function () {
    closeRatingModal(); // 提交後關閉模態框
};
