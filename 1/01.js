function selectText(x) {
    if (document.selection) {
        var range = document.body.createTextRange();
        range.moveToElementText(x);
        range.select();
    } else if (window.getSelection) {
        var selection = window.getSelection();
        var range = document.createRange();
        selection.removeAllRanges();
        range.selectNodeContents(x);
        selection.addRange(range);
    }
}
function cp(x)
{
    selectText(x);
    document.execCommand("copy");
    alert("复制成功,快去分享好友吧")
}

