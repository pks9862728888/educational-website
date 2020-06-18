import { FormGroup, ValidatorFn, ValidationErrors, FormControl } from '@angular/forms';

// Generates error if passwords do not match.
export const passwordMatchValidator: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    return password.value === confirmPassword.value ? null : { mismatch: true };

};

// Generates error if username and password are similar
export const usernamePasswordValidator: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
    const username = control.get('username');
    const password = control.get('password');

    if (username.pristine || password.pristine) {
        return null;
    }

    return password.value === username.value ? { usernamePasswordSame : true } : null;
};

// Generates error if date is valid or not
// export const isValidDate = (c: FormControl) => {
//     const DATE_REGEXP = /^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/;
//     return DATE_REGEXP.test(c.value) || c.value === '' ? null : {invalidDate: true};
// };
