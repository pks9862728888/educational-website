import { UiService } from './../../services/ui.service';
import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { ApiService } from '../../services/api.service';
import { GENDER, COUNTRY, LANGUAGE, LANGUAGE_REVERSE, GENDER_REVERSE, COUNTRY_REVERSE } from '../../../constants';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { UploadProfilePictureComponent } from './upload-profile-picture/upload-profile-picture.component';
import { ChooseFromExistingComponent } from './choose-from-existing/choose-from-existing.component';
import { formatDate } from '../../format-datepicker';

interface TeacherProfileDetails {
  id: number;
  email: string;
  username: string;
  created_date: string;
  user_profile: {
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

interface DeletedCurrentPictureResponse {
  deleted: boolean;
  class_profile_picture_deleted: boolean;
  public_profile_picture_deleted: boolean;
}

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
  profilePictureCount: number;

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
               private uiService: UiService,
               private formBuilder: FormBuilder,
               private dialog: MatDialog ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
    this.maxDate = new Date();         // For selecting max date as today
  }

  ngOnInit(): void {
    this.apiService.getTeacherProfile().subscribe(
      (result: TeacherProfileDetails) => {
        // Setting data in session storage and local variable
        sessionStorage.setItem('user_id', JSON.stringify(result.id));
        this.email = result.email;
        sessionStorage.setItem('email', result.email);
        this.username = result.username;
        sessionStorage.setItem('username', result.username);

        this.createdDate = result.created_date;
        sessionStorage.setItem('created_date', result.created_date);

        if (result.user_profile.country) {
          this.country = COUNTRY[result.user_profile.country];
          sessionStorage.setItem('country', this.country);
        }

        if (result.user_profile.date_of_birth) {
          this.dateOfBirth = result.user_profile.date_of_birth;
          sessionStorage.setItem('date_of_birth', result.user_profile.date_of_birth);
        }

        if (result.user_profile.first_name) {
          this.firstName = result.user_profile.first_name;
          sessionStorage.setItem('first_name', result.user_profile.first_name);
        }

        if (result.user_profile.last_name) {
          this.lastName = result.user_profile.last_name;
          sessionStorage.setItem('last_name', result.user_profile.last_name);
        }

        if (result.user_profile.gender) {
          this.gender = GENDER[result.user_profile.gender];
          sessionStorage.setItem('gender', this.gender);
        }

        if (result.user_profile.phone) {
          this.phone = result.user_profile.phone;
          sessionStorage.setItem('phone', result.user_profile.phone);
        }

        this.primaryLanguage = LANGUAGE[result.user_profile.primary_language];
        sessionStorage.setItem('primary_language', this.primaryLanguage);

        if (result.user_profile.secondary_language) {
          this.secondaryLanguage = LANGUAGE[result.user_profile.secondary_language];
          sessionStorage.setItem('secondary_language', this.secondaryLanguage);
        }

        if (result.user_profile.tertiary_language) {
          this.tertiaryLanguage = LANGUAGE[result.user_profile.tertiary_language];
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
      errors => {}
    );

    // For getting the total number of profile picture count from server
    this.apiService.getProfilePictureCount().subscribe(
      (result: {count: number; }) => {
        this.profilePictureCount = result.count;
      },
      error => {}
    );
  }

  createEditProfileForm() {
    this.editProfileForm = this.formBuilder.group({
      username: [this.username, [
        Validators.required,
        Validators.minLength(4),
        Validators.maxLength(30)
      ]],
      user_profile: this.formBuilder.group({
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
      user_profile: {
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
    if (editProfileDetailsData.user_profile.date_of_birth) {
      // Formatting date of birth in YYYY-MM-DD
      editProfileDetailsData.user_profile.date_of_birth = formatDate(this.editProfileForm.value.user_profile.date_of_birth);
    }

    this.apiService.patchTeacherProfileDetails(editProfileDetailsData).subscribe(
      (result: TeacherProfileDetails ) => {
        this.username = result.username;
        sessionStorage.setItem('username', result.username);

        this.country = COUNTRY[result.user_profile.country];
        sessionStorage.setItem('country', this.country);

        this.dateOfBirth = result.user_profile.date_of_birth;
        sessionStorage.setItem('date_of_birth', result.user_profile.date_of_birth);

        this.firstName = result.user_profile.first_name;
        sessionStorage.setItem('first_name', result.user_profile.first_name);

        this.lastName = result.user_profile.last_name;
        sessionStorage.setItem('last_name', result.user_profile.last_name);

        this.gender = GENDER[result.user_profile.gender];
        sessionStorage.setItem('gender', this.gender);

        this.phone = result.user_profile.phone;
        sessionStorage.setItem('phone', result.user_profile.phone);

        this.primaryLanguage = LANGUAGE[result.user_profile.primary_language];
        sessionStorage.setItem('primary_language', this.primaryLanguage);

        this.secondaryLanguage = LANGUAGE[result.user_profile.secondary_language];
        sessionStorage.setItem('secondary_language', this.secondaryLanguage);

        this.tertiaryLanguage = LANGUAGE[result.user_profile.tertiary_language];
        sessionStorage.setItem('tertiary_language', this.tertiaryLanguage);
        this.uiService.showSnackBar('Profile details updated successfully!', 2000);

        // Closing edit view
        this.editProfile = !this.editProfile;
      },
      errors => {
        if (errors.error) {
          if (errors.error.user_profile.phone) {
            this.phoneNumberError = errors.error.user_profile.phone[0];
          }
          if (errors.error.username) {
            this.usernameError = errors.error.username[0];
          }
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
    const dialogRef = this.dialog.open(UploadProfilePictureComponent);

    dialogRef.afterClosed().subscribe(result => {
      // status is true if profile picture is successfully uploaded else false
      if (result.status) {
        this.uiService.showSnackBar('Profile picture uploaded successfully!', 2000);

        // Update the appropriate control variables
        if (result.classProfilePictureChanged) {
          this.classProfilePicture = sessionStorage.getItem('class_profile_picture');
          this.classProfilePictureUploadedOn = sessionStorage.getItem('class_profile_picture_uploaded_on');

          // Updating total profile picture count
          this.profilePictureCount += 1;
        }
      }
    });
  }

  // To delete the current active class profile picture
  deleteCurrentPicture() {
    const id = sessionStorage.getItem('class_profile_picture_id');

    this.apiService.deleteCurrentProfilePicture(id).subscribe(
      (response: DeletedCurrentPictureResponse) => {

        // Removing the deleted data from session storage
        if (response.deleted === true) {
          if (response.class_profile_picture_deleted === true) {
            sessionStorage.removeItem('class_profile_picture');
            sessionStorage.removeItem('class_profile_picture_id');
            sessionStorage.removeItem('class_profile_picture_uploaded_on');
            this.classProfilePicture = null;
          }
          if (response.class_profile_picture_deleted === true) {
            sessionStorage.removeItem('public_profile_picture');
            sessionStorage.removeItem('public_profile_picture_id');
            sessionStorage.removeItem('public_profile_picture_uploaded_on');
          }

          // Updating total profile picture count
          this.profilePictureCount -= 1;
          this.editProfilePicture = false;
        }
        this.uiService.showSnackBar('Successfully deleted current profile picture.', 2000);
      },
      error => {
        if (error.error.deleted === false) {
          this.uiService.showSnackBar('Internal server error. Unable to delete picture.', 2000);
          console.error(error.message);
        }

        if (error.error.id) {
          console.error('Unable to delete picture. ' + error.error.id[0]);
        }
      }
    );
  }

  // To remove the current active class profile picture
  removeCurrentPicture() {
    this.apiService.removeCurrentClassProfilePicture().subscribe(
      (response: {removed: boolean; } ) => {
        if (response.removed === true) {
          this.classProfilePicture = null;
          this.classProfilePictureUploadedOn = null;
          sessionStorage.removeItem('class_profile_picture_id');
          sessionStorage.removeItem('class_profile_picture');
          sessionStorage.removeItem('class_profile_picture_uploaded_on');
        }
        this.editProfilePicture = false;
      },
      error => {
        console.log(error);
      }
    );
  }

  // To choose from existing profile picture
  chooseFromExistingClicked() {
    const dialogRef = this.dialog.open(ChooseFromExistingComponent);

    dialogRef.afterClosed().subscribe(result => {
      // status is true if profile picture is successfully uploaded else false
      if (result.status) {
        this.uiService.showSnackBar('Profile picture changed successfully!', 2000);
        // Update the appropriate control variables
        if (result.classProfilePictureChanged) {
          this.classProfilePicture = sessionStorage.getItem('class_profile_picture');
          this.classProfilePictureUploadedOn = sessionStorage.getItem('class_profile_picture_uploaded_on');
        }
      }

      this.editProfilePicture = false;
    });
  }
}
