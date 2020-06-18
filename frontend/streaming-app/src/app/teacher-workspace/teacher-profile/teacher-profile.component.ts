import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { ApiService } from '../../api.service';
import { GENDER, COUNTRY, LANGUAGE, LANGUAGE_REVERSE, GENDER_REVERSE, COUNTRY_REVERSE } from '../../../constants';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

interface TeacherProfileDetails {
  id: number;
  email: string;
  username: string;
  created_date: string;
  teacher_profile: {
    first_name: string;
    last_name: string;
    gender: string;
    phone: string;
    country: string;
    date_of_birth: string;
    primary_language: string;
    secondary_language: string;
    tertiary_language: string;
  };
  profile_pictures: {
    id: number;
    image: string;
    uploaded_on: string;
    public_profile_picture: boolean;
    class_profile_picture: boolean;
  };
}

@Component({
  template: `
    <div class="snackbar-text">
      Profile details updated successfully!
    </div>
  `,
  styles: [`
    .snackbar-text {
      color: yellow;
      text-align: center;
    }
  `]
})
export class ProfileDetailsUpdatedComponent {}


@Component({
  selector: 'app-teacher-profile',
  templateUrl: './teacher-profile.component.html',
  styleUrls: ['./teacher-profile.component.css']
})
export class TeacherProfileComponent implements OnInit {

  // For detecting whether device is mobile
  mobileQuery: MediaQueryList;

  // For controlling edit views
  editProfile = false;
  editAccount = false;
  editProfilePicture = false;
  uploadProfilePicture = false;

  // Edit Forms
  editProfileForm: FormGroup;

  // Response data of user profile
  email: string;
  username: string;
  createdDate: string;
  country: string;
  dateOfBirth: string;
  firstName: string;
  lastName: string;
  gender: string;
  phone: string;
  primaryLanguage: string;
  secondaryLanguage: string;
  tertiaryLanguage: string;
  classProfilePicture: string;
  classProfilePictureUploadedOn: string;

  // For showing errors
  usernameError: string;
  phoneNumberError: string;

  // Controls the maximum date of birth allowed
  maxDate: Date;

  constructor( private media: MediaMatcher,
               private apiService: ApiService,
               private formBuilder: FormBuilder,
               private snackBar: MatSnackBar ) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this.maxDate = new Date();         // For selecting max date as today
  }

  ngOnInit(): void {
    // For getting profile data from server
    if (sessionStorage.getItem('country')) {          // Assuming country will be set initially for all teacher
      this.email = sessionStorage.getItem('email');
      this.username = sessionStorage.getItem('username');
      this.createdDate = sessionStorage.getItem('created_date');
      this.country = sessionStorage.getItem('country');
      this.dateOfBirth = sessionStorage.getItem('date_of_birth');
      this.firstName = sessionStorage.getItem('first_name');
      this.lastName = sessionStorage.getItem('last_name');
      this.gender = sessionStorage.getItem('gender');
      this.phone = sessionStorage.getItem('phone');
      this.primaryLanguage = sessionStorage.getItem('primary_language');
      this.secondaryLanguage = sessionStorage.getItem('secondary_language');
      this.tertiaryLanguage = sessionStorage.getItem('tertiary_language');
      this.classProfilePicture = sessionStorage.getItem('class_profile_picture');
      this.classProfilePictureUploadedOn = sessionStorage.getItem('class_profile_picture_uploaded_on');

    } else {                                         // This will only be requested for first run
      this.apiService.getTeacherProfile().subscribe(
        (result: TeacherProfileDetails) => {
          console.log(result);
          // Setting data in session storage and local variable
          sessionStorage.setItem('user_id', JSON.stringify(result.id));
          this.email = result.email;
          sessionStorage.setItem('email', result.email);
          this.username = result.username;
          sessionStorage.setItem('username', result.username);

          this.createdDate = result.created_date;
          sessionStorage.setItem('created_date', result.created_date);

          if (result.teacher_profile.country) {
            this.country = COUNTRY[result.teacher_profile.country];
            sessionStorage.setItem('country', this.country);
          }

          if (result.teacher_profile.date_of_birth) {
            this.dateOfBirth = result.teacher_profile.date_of_birth;
            sessionStorage.setItem('date_of_birth', result.teacher_profile.date_of_birth);
          }

          if (result.teacher_profile.first_name) {
            this.firstName = result.teacher_profile.first_name;
            sessionStorage.setItem('first_name', result.teacher_profile.first_name);
          }

          if (result.teacher_profile.last_name) {
            this.lastName = result.teacher_profile.last_name;
            sessionStorage.setItem('last_name', result.teacher_profile.last_name);
          }

          if (result.teacher_profile.gender) {
            this.gender = GENDER[result.teacher_profile.gender];
            sessionStorage.setItem('gender', this.gender);
          }

          if (result.teacher_profile.phone) {
            this.phone = result.teacher_profile.phone;
            sessionStorage.setItem('phone', result.teacher_profile.phone);
          }

          this.primaryLanguage = LANGUAGE[result.teacher_profile.primary_language];
          sessionStorage.setItem('primary_language', this.primaryLanguage);

          if (result.teacher_profile.secondary_language) {
            this.secondaryLanguage = LANGUAGE[result.teacher_profile.secondary_language];
            sessionStorage.setItem('secondary_language', this.secondaryLanguage);
          }

          if (result.teacher_profile.tertiary_language) {
            this.tertiaryLanguage = LANGUAGE[result.teacher_profile.tertiary_language];
            sessionStorage.setItem('tertiary_language', this.tertiaryLanguage);
          }

          if (result.profile_pictures.class_profile_picture === true) {
            this.classProfilePicture = result.profile_pictures.image;
            this.classProfilePictureUploadedOn = result.profile_pictures.uploaded_on;
            sessionStorage.setItem('class_profile_picture_id', JSON.stringify(result.profile_pictures.id));
            sessionStorage.setItem('class_profile_picture', this.classProfilePicture);
            sessionStorage.setItem('class_profile_picture_uploaded_on', this.classProfilePictureUploadedOn);
          }

          if (result.profile_pictures.public_profile_picture === true) {
            sessionStorage.setItem('public_profile_picture_id', JSON.stringify(result.profile_pictures.id));
            sessionStorage.setItem('public_profile_picture', result.profile_pictures.image);
            sessionStorage.setItem('public_profile_picture_uploaded_on', result.profile_pictures.uploaded_on);
          }
        },
        errors => {
          console.error(errors);
        }
      );
    }
  }

  createEditProfileForm() {
    this.editProfileForm = this.formBuilder.group({
      username: [this.username, [
        Validators.required,
        Validators.minLength(4),
        Validators.maxLength(30)
      ]],
      teacher_profile: this.formBuilder.group({
        first_name: [this.firstName, ],
        last_name: [this.lastName, ],
        phone: [this.phone, ],
        gender: [GENDER_REVERSE[this.gender], ],
        country: [COUNTRY_REVERSE[this.country], ],
        date_of_birth: [this.dateOfBirth, ],
        primary_language: [LANGUAGE_REVERSE[this.primaryLanguage], ],
        secondary_language: [LANGUAGE_REVERSE[this.secondaryLanguage], ],
        tertiary_language: [LANGUAGE_REVERSE[this.tertiaryLanguage], ]
      })
    });
  }

  editProfileClicked() {
    if (this.editProfile === false) {
      this.createEditProfileForm();
    }
    this.editProfile = !this.editProfile;
  }

  profileDetailsReset() {
    this.editProfileForm.patchValue({
      username: this.username,
      teacher_profile: {
        first_name: this.firstName,
        last_name: this.lastName,
        phone: this.phone,
        gender: GENDER_REVERSE[this.gender],
        country: COUNTRY_REVERSE[this.country],
        date_of_birth: this.dateOfBirth,
        primary_language: LANGUAGE_REVERSE[this.primaryLanguage],
        secondary_language: LANGUAGE_REVERSE[this.secondaryLanguage],
        tertiary_language: LANGUAGE_REVERSE[this.tertiaryLanguage]
      }
    });
  }

  profileDetailsSubmit() {
    const editProfileDetailsData = this.editProfileForm.value;
    if (editProfileDetailsData.teacher_profile.date_of_birth) {
      // Formatting date of birth in YYYY-MM-DD
      const date = new Date(this.editProfileForm.value.teacher_profile.date_of_birth);
      let month = '' + (date.getMonth() + 1);
      let day = '' + date.getDate();
      if (month.length < 2) {
        month = '0' + month;
      }
      if (day.length < 2) {
          day = '0' + day;
      }
      const dateFormatted = date.getFullYear() + '-' + month + '-' + day;
      editProfileDetailsData.teacher_profile.date_of_birth = dateFormatted;
    }

    this.apiService.patchTeacherProfileDetails(editProfileDetailsData).subscribe(
      (result: TeacherProfileDetails ) => {
        console.log(result);

        this.username = result.username;
        sessionStorage.setItem('username', result.username);

        if (result.teacher_profile.country) {
          this.country = COUNTRY[result.teacher_profile.country];
          sessionStorage.setItem('country', this.country);
        }

        if (result.teacher_profile.date_of_birth) {
          this.dateOfBirth = result.teacher_profile.date_of_birth;
          sessionStorage.setItem('date_of_birth', result.teacher_profile.date_of_birth);
        }

        if (result.teacher_profile.first_name) {
          this.firstName = result.teacher_profile.first_name;
          sessionStorage.setItem('first_name', result.teacher_profile.first_name);
        }

        if (result.teacher_profile.last_name) {
          this.lastName = result.teacher_profile.last_name;
          sessionStorage.setItem('last_name', result.teacher_profile.last_name);
        }

        if (result.teacher_profile.gender) {
          this.gender = GENDER[result.teacher_profile.gender];
          sessionStorage.setItem('gender', this.gender);
        }

        if (result.teacher_profile.phone) {
          this.phone = result.teacher_profile.phone;
          sessionStorage.setItem('phone', result.teacher_profile.phone);
        }

        this.primaryLanguage = LANGUAGE[result.teacher_profile.primary_language];
        sessionStorage.setItem('primary_language', this.primaryLanguage);

        if (result.teacher_profile.secondary_language) {
          this.secondaryLanguage = LANGUAGE[result.teacher_profile.secondary_language];
          sessionStorage.setItem('secondary_language', this.secondaryLanguage);
        }

        if (result.teacher_profile.tertiary_language) {
          this.tertiaryLanguage = LANGUAGE[result.teacher_profile.tertiary_language];
          sessionStorage.setItem('tertiary_language', this.tertiaryLanguage);
        }

        // Displaying appropriate message
        this.snackBar.openFromComponent(ProfileDetailsUpdatedComponent, {
          duration: 2000
        });

        // Closing edit view
        this.editProfile = !this.editProfile;
      },
      errors => {
        if (errors.error.teacher_profile.phone) {
          this.phoneNumberError = errors.error.teacher_profile.phone[0];
        }
        if (errors.error.username) {
          this.usernameError = errors.error.username[0];
        }

      }
    );
  }

  editAccountClicked() {
    this.editAccount = !this.editAccount;
  }

  openEditProfilePictureDialog() {
    this.editProfilePicture = !this.editProfilePicture;
  }

  openUploadPictureDialog() {
    this.uploadProfilePicture = true;
  }

}
