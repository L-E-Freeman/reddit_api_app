function refreshIndex() {

    console.log("button success")

    var request = new XMLHttpRequest();
    // Pass in correct URL here.
    request.open('GET', '');

    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            console.log("onload success")
            var resp = this.response;
            
            for (let post of resp) {
                var a = document.createElement('a');
                var linkText = document.createTextNode(post.post_title)
                a.appendChild(linkText)
                a.href = post.post_id
                document.body.appendChild(a);
            }

        } else { 
            console.log("Status code error")
        }
    }
};

