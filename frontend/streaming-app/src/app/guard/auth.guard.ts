import { AuthService } from '../services/auth.service';
import { authTokenName, INSTITUTE_TYPE_REVERSE } from './../../constants';
import { CookieService } from 'ngx-cookie-service';
import { Router, CanLoad } from '@angular/router';
import { Injectable } from '@angular/core';
import { Route } from '@angular/compiler/src/core';


// @Injectable()
// export class SignUpLoginGuard implements CanLoad {

//   constructor( private cookieService: CookieService,
//                private authService: AuthService ) {}

//   canLoad(route: Route) {
//       if (this.cookieService.get(authTokenName)) {
//         this.authService.logout();
//       }
//       return true;
//   }
// }


@Injectable()
export class StudentWorkspaceGuard implements CanLoad {

  constructor( private cookieService: CookieService,
               private authService: AuthService,
               private router: Router ) {}

  canLoad(route: Route) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('is_student') === 'true') {
          return true;
        } else {
          this.authService.logout();
          this.router.navigate(['/auth/login']);
        }
      } else {
        this.router.navigate(['/auth/login']);
      }
  }
}


@Injectable()
export class TeacherWorkspaceGuard implements CanLoad {

  constructor( private cookieService: CookieService,
               private authService: AuthService,
               private router: Router ) {}

  canLoad(route: Route) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('is_teacher') === 'true') {
          return true;
        } else {
          this.authService.logout();
          this.router.navigate(['/auth/login']);
        }
      } else {
        this.router.navigate(['/auth/login']);
      }
  }
}


@Injectable()
export class StaffWorkspaceGuard implements CanLoad {

  constructor( private cookieService: CookieService,
               private authService: AuthService,
               private router: Router ) {}

  canLoad(route: Route) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('is_staff') === 'true') {
          return true;
        } else {
          this.authService.logout();
          this.router.navigate(['/auth/login']);
        }
      } else {
        this.router.navigate(['/auth/login']);
      }
  }
}


@Injectable()
export class SchoolWorkspaceGuard implements CanLoad {

  constructor( private cookieService: CookieService,
               private router: Router ) {}

  canLoad(route: Route) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('activeRoute') &&
            sessionStorage.getItem('currentInstituteRole') &&
            sessionStorage.getItem('currentInstituteSlug') &&
            sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE['School']) {
          return true;
        } else {
          sessionStorage.setItem('activeRoute', 'INSTITUTES');
          this.router.navigate(['/teacher-workspace/institutes']);
        }
      } else {
        this.router.navigate(['/auth/login']);
      }
  }
}


@Injectable()
export class CollegeWorkspaceGuard implements CanLoad {

  constructor( private cookieService: CookieService,
               private router: Router ) {}

  canLoad(route: Route) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('activeRoute') &&
            sessionStorage.getItem('currentInstituteRole') &&
            sessionStorage.getItem('currentInstituteSlug') &&
            sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE['College']) {
          return true;
        } else {
          sessionStorage.setItem('activeRoute', 'INSTITUTES');
          this.router.navigate(['/teacher-workspace/institutes']);
        }
      } else {
        this.router.navigate(['/auth/login']);
      }
  }
}


@Injectable()
export class CoachingWorkspaceGuard implements CanLoad {

  constructor( private cookieService: CookieService,
               private router: Router ) {}

  canLoad(route: Route) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('activeRoute') &&
            sessionStorage.getItem('currentInstituteRole') &&
            sessionStorage.getItem('currentInstituteSlug') &&
            sessionStorage.getItem('currentInstituteType') === INSTITUTE_TYPE_REVERSE['Coaching']) {
          return true;
        } else {
          sessionStorage.setItem('activeRoute', 'INSTITUTES');
          this.router.navigate(['/teacher-workspace/institutes']);
        }
      } else {
        this.router.navigate(['/auth/login']);
      }
  }
}
