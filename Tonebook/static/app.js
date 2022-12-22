let editor;
let vue

window.addEventListener("load", ()=>{
    // initialise editor if exists.
    let loadEditor = content => {
        if(!document.getElementById("editorjs")) {
            return;
        }

        let data = {
            selector: "#editorjs",
            plugins: [
              'a11ychecker','advlist','advcode','advtable','autolink','checklist','export',
              'lists','link','image','charmap','preview','anchor','searchreplace','visualblocks',
              'powerpaste','fullscreen','formatpainter','insertdatetime','media','table','help','wordcount'
            ],
            toolbar: 'undo redo | formatpainter casechange blocks | bold italic backcolor | ' +
              'alignleft aligncenter alignright alignjustify | ' +
              'bullist numlist checklist outdent indent | removeformat | a11ycheck code table help'
        };

        if(content && typeof content === "string" && content !== "") {
            data.setup = (editor)=>{
                editor.on('init', () => {
                    if(content && typeof content == "string" && content !== "") {
                        editor.setContent(content);
                    }
                });
            }
        }

        editor = tinymce.init(data);
        console.log("ahh");
    };

    let setContent = content => {
        try {
            tinymce.get("editorjs").setContent(content);
            return true;
        } catch(e) {}

        return false;
    };

    let getContent = () => {
        try {
            return tinymce.get("editorjs").getContent();
        } catch(e) {}

        return "";
    };

    vue = Vue.createApp({
        delimiters: ["[[", "]]"],
        data() {
            return {
                user: false,
                message: "",
                action_file: {
                    data: false,
                    name: "",
                },
                edit_file_data: false
            }
        },
        methods: {
            async getUser() {
                let response = await fetch("/user/", {
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken":document.querySelector("[name=csrfmiddlewaretoken]").value,
                    }
                }).then(response => response.json());

                if(response.user) {
                    this.user = response.user;
                }
            },
            async createFile() {
                let response = await fetch("../create/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken":document.querySelector("[name=csrfmiddlewaretoken]").value,
                    },
                    body: JSON.stringify({
                        name: this.action_file.name
                    })
                }).then(response => response.json());

                if(response.user) {
                    this.user = response.user;
                    this.message = "The file was created successfully.";
                } else if(response.error) {
                    this.message = response.error;
                } else {
                    this.message = "An Error has occurred";
                }
            },
            async renameFile(file) {
                let response = await fetch(file.rename, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken":document.querySelector("[name=csrfmiddlewaretoken]").value,
                    },
                    body: JSON.stringify({
                        name: this.action_file.name
                    })
                }).then(response => response.json());

                if(response.user) {
                    this.user = response.user;
                    this.message = "The file was renamed successfully.";
                } else if(response.error) {
                    this.message = response.error;
                } else {
                    this.message = "An Error has occurred";
                }
            },
            async deleteFile(file) {
                let response = await fetch(file.delete, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken":document.querySelector("[name=csrfmiddlewaretoken]").value,
                    },
                    body: JSON.stringify({
                        name: this.action_file.name
                    })
                }).then(response => response.json());

                if(response.user) {
                    this.user = response.user;
                    this.message = "The file was deleted successfully.";
                } else if(response.error) {
                    this.message = response.error;
                } else {
                    this.message = "An Error has occurred";
                }
            },
            async saveFile() {
                let response = await fetch(this.edit_file_data.save, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken":document.querySelector("[name=csrfmiddlewaretoken]").value,
                    },
                    body: JSON.stringify({
                        content: getContent()
                    })
                }).then(response => response.json());

                if(response.user) {
                    this.user = response.user;
                    this.message = "The file was saved successfully.";
                } else if(response.error) {
                    this.message = response.error;
                } else {
                    this.message = "An Error has occurred";
                }
            },
            editMode(data) {
                try {
                    this.edit_file_data = data;
                    loadEditor(data.content);
                } catch(e) {
                    this.message = "Couldn't load the file at this point of time";
                }
            },
            friendlyDateTime(data) {
                let date = new Date(data);
                let d = date.getDate();
                let mo = date.getMonth();
                let y = date.getFullYear();
                let h = date.getHours();
                let mi = date.getMinutes();
                let s = date.getSeconds();

                if(d < 10) {
                    d = "0" + d;
                }

                if(mo < 10) {
                    mo = "0" + mo;
                }

                if(h < 10) {
                    h = "0" + h;
                }

                if(mi < 10) {
                    mi = "0" + mi;
                }

                if(s < 10) {
                    s = "0" + s;
                }

                return d +"/"+ mo+"/"+y+" "+h+":"+mi+":"+s;
            },
            clearFileActions() {
                this.action_file = {
                    data: false,
                    name: ""
                }
            }
        },
        async created() {
            await this.getUser();
        }
    });

    vue.mount(".main");
});
