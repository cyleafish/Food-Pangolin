function confirmOrder(url) {
    if (confirm("確定接單嗎？")) {
        // 直接使用傳入的 URL
        window.location.href = url;
    }
}


function openRatingModal(url) { 
    // 將表單的 action 設置為生成的 URL
    document.getElementById('ratingForm').action = url;
    document.getElementById('ratingModal').style.display = 'block';
}



function closeRatingModal() {
    // 隱藏模態框
    document.getElementById('ratingModal').style.display = 'none';
}

document.getElementById('ratingForm').onsubmit = function () {
    closeRatingModal(); // 提交後關閉模態框
};
