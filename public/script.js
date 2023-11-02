const showPassword = (fieldID) => {
    // shows the password in plain text instead on dots
    const field = document.getElementById(fieldID);
    field.type = 'text';
};
const hidePassword = (fieldID) => {
    // hides the password and shows dots
    const field = document.getElementById(fieldID);
    field.type = 'password';
};

const processFormData = () => {
    // get form data from the fields in the form
    const form = document.getElementById('form');
    const formData = new FormData(form);
    console.log(formData);
};
