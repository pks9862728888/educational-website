import { FormGroup, ValidatorFn, ValidationErrors, FormControl, AbstractControl } from '@angular/forms';

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


export function postiveIntegerValidator(control: AbstractControl): {[key: string]: boolean} | null  {
  if (control.pristine || control.value > 0) {
    return null;
  }
  return { postiveIntegerValidator: true };
}


export function isNumberValidator(control: AbstractControl): {[key: string]: boolean} | null {
  if (control.pristine || control.value >= 0) {
    return null;
  }
  return { isNumberValidator: true };
}

export function islengthWithin20Validator(control: AbstractControl): {[key: string]: boolean} | null {
  if (control.pristine || control.value.length <= 20) {
    return null;
  }
  return { islengthWithin20Validator: true };
}
