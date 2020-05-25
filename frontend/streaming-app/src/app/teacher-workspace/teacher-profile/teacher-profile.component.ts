import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { ApiService } from '../../api.service';
import { GENDER, COUNTRY, LANGUAGE } from '../../../constants';

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
  selector: 'app-teacher-profile',
  templateUrl: './teacher-profile.component.html',
  styleUrls: ['./teacher-profile.component.css']
})
export class TeacherProfileComponent implements OnInit {

  // For detecting whether device is mobile
  mobileQuery: MediaQueryList;

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

  constructor( private media: MediaMatcher,
               private apiService: ApiService ) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
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

          if (result.teacher_profile.last_name) {
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

}
