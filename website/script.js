var date = new Date();
var now = date.getTime();
const select_file_type = document.querySelector("#select-type");
const select_images = document.querySelector("#form-select-images");
const select_video = document.querySelector("#form-select-video");
console.log(now);

function change_visibility(divName, hide) {
    if (hide == true) {
        document.getElementById(divName).setAttribute("hidden","");
    } else {
        document.getElementById(divName).removeAttribute("hidden");
    }
}


document.forms['form-images'].addEventListener('submit', (event) => {
    formData = new FormData(event.target);
    formData.append('time', now);
    event.preventDefault();
    console.log('Clicked');
    console.log(event);
    change_visibility("spinner-images", false)
    fetch(event.target.action, {
        method: 'POST',
        body: formData // event.target is the form
    }).then((resp) => {
        change_visibility("spinner-images", true)
        return resp.json(); // or resp.text() or whatever the server sends
    }).then((body) => {
        console.log(body)
    }).catch((error) => {
        console.log(error)
    });
});

document.forms['form-video'].addEventListener('submit', (event) => {
    formData = new FormData(event.target);
    formData.append('time', now);
    event.preventDefault();
    console.log('Clicked');
    console.log(event);
    change_visibility("spinner-video", false)
    fetch(event.target.action, {
        method: 'POST',
        body: formData // event.target is the form
    }).then((resp) => {
        change_visibility("spinner-video", true)
        return resp.json(); // or resp.text() or whatever the server sends
    }).then((body) => {
        console.log(body)
    }).catch((error) => {
        console.log(error)
    });
});

const displayWhenSelected = (source, value, target) => {
    const selectedIndex = source.selectedIndex;
    const isSelected = source[selectedIndex].value === value;
    target.classList[isSelected
        ? "add"
        : "remove"
    ]("show");
};
select_file_type.addEventListener("change", (evt) =>
    displayWhenSelected(select_file_type, "image", select_images)
);

select_file_type.addEventListener("change", (evt) =>
    displayWhenSelected(select_file_type, "video", select_video)
);

function check_empty_images() {
    let images = document.getElementById("image-file").files;
    let background = document.getElementById("image-file-background").files;
    let quality = document.querySelector('input[name="inlineRadioOptions"]:checked');
    const button = document.getElementById('upload-images');
    console.log(quality, images, background);


    if (images.length > 0 && background.length > 0) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }
}

function check_empty_video() {
    let video = document.getElementById("video-file").files;
    let background = document.getElementById("video-file-background").files;
    let quality = document.querySelector('input[name="inlineRadioOptions"]:checked');
    const button = document.getElementById('upload-video');
    console.log(quality, video, background)


    if (video.length > 0 && background.length > 0) {
        button.disabled = false;
    } else {
        button.disabled = true;
    }
}