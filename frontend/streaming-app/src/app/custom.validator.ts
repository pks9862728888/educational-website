import { FormGroup, ValidatorFn, ValidationErrors, FormControl, AbstractControl } from '@angular/forms';
import { QUESTION_SECTION_VIEW_TYPE } from 'src/constants';

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
  if (control.pristine || Number.isInteger(+control.value) && +control.value > 0) {
    return null;
  }
  return { postiveIntegerValidator: true };
}


export function isNumberValidator(control: AbstractControl): {[key: string]: boolean} | null {
  if (control.pristine || !Number.isNaN(+control.value)) {
    return null;
  }
  return { isNumberValidator: true };
}

export function characterLengthLessThanEqualTo(value: number): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    if (control.pristine || control.value.length <= value) {
      return null;
    }
    return { characterLengthLessThanEqualTo: true };
  };
}

export const addQuestionFormValidator: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
  const noOfQuestionToAttempt = +control.get('no_of_question_to_attempt').value;
  const answerAllQuestions = control.get('answer_all_questions').value;
  const view = control.get('view').value;

  if (!Number.isInteger(noOfQuestionToAttempt)) {
    return { numberShouldBeInteger: true };
  }

  if (view === QUESTION_SECTION_VIEW_TYPE.MULTIPLE_QUESTION) {
    if (answerAllQuestions === false && noOfQuestionToAttempt === 0) {
      return { numberShouldBeGreaterThanZeroError: true };
    }
  }
  return null;
};

export const fillInTheBlankFormValidator: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
  const manualChecking = control.get('manual_checking').value;
  const correctAnswer = control.get('correct_answer').value;

  if (!manualChecking && !correctAnswer) {
    return { fillInTheBlankFormValidator: true };
  }

  return null;
};
