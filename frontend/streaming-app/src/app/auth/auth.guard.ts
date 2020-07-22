import { AuthService } from 'src/app/auth.service';
import { authTokenName, INSTITUTE_TYPE, INSTITUTE_TYPE_REVERSE } from './../../constants';
import { CookieService } from 'ngx-cookie-service';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Injectable } from '@angular/core';


@Injectable()
export class SignUpLoginGuard implements CanActivate {

  constructor( private cookieService: CookieService,
               private authService: AuthService ) {}

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot) {
      if (this.cookieService.get(authTokenName)) {
        this.authService.logout();
      }
      return true;
  }
}


@Injectable()
export class StudentWorkspaceGuard implements CanActivate {

  constructor( private cookieService: CookieService,
               private authService: AuthService,
               private router: Router ) {}

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('is_student') === 'true') {
          return true;
        } else {
          this.authService.logout();
          this.router.navigate(['/login']);
        }
      } else {
        this.router.navigate(['/login']);
      }
  }
}


@Injectable()
export class TeacherWorkspaceGuard implements CanActivate {

  constructor( private cookieService: CookieService,
               private authService: AuthService,
               private router: Router ) {}

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('is_teacher') === 'true') {
          return true;
        } else {
          this.authService.logout();
          this.router.navigate(['/login']);
        }
      } else {
        this.router.navigate(['/login']);
      }
  }
}


@Injectable()
export class StaffWorkspaceGuard implements CanActivate {

  constructor( private cookieService: CookieService,
               private authService: AuthService,
               private router: Router ) {}

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot) {
      if (this.cookieService.get(authTokenName)) {
        if (sessionStorage.getItem('is_staff') === 'true') {
          return true;
        } else {
          this.authService.logout();
          this.router.navigate(['/login']);
        }
      } else {
        this.router.navigate(['/login']);
      }
  }
}


@Injectable()
export class SchoolWorkspaceGuard implements CanActivate {

  constructor( private cookieService: CookieService,
               private router: Router ) {}

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot) {
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
        this.router.navigate(['/login']);
      }
  }
}


@Injectable()
export class CollegeWorkspaceGuard implements CanActivate {

  constructor( private cookieService: CookieService,
               private router: Router ) {}

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot) {
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
        this.router.navigate(['/login']);
      }
  }
}


@Injectable()
export class CoachingWorkspaceGuard implements CanActivate {

  constructor( private cookieService: CookieService,
               private router: Router ) {}

  canActivate(route: ActivatedRouteSnapshot,
              state: RouterStateSnapshot) {
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
        this.router.navigate(['/login']);
      }
  }
}
