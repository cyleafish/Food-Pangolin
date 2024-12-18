function confirmOrder(orderId) {
    if (confirm("確定接單嗎？")) {
        // 跳轉到接單的路由
        window.location.href = `/accept_order?order_id=${orderId}`;
    }
}
