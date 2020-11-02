import { Route } from '@angular/compiler/src/core';
import { INSTITUTE_TYPE_REVERSE,
         currentInstituteSlug,
         currentInstituteType,
         currentClassSlug,
         currentInstituteRole } from './../../constants';
import { CanActivate,
         ActivatedRouteSnapshot,
         RouterStateSnapshot,
         Router,
         CanLoad } from '@angular/router';
import { Injectable } from '@angular/core';


// @Injectable()
// export class InstituteRoutingGuard implements CanActivate {
//   // Activates link if unexpired license exists
//   constructor(private router: Router) {}

//   canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
//     if (sessionStorage.getItem(purchasedLicenseExists) === 'true') {
//       return true;
//     } else {
//       const currentInstituteSlug_ = sessionStorage.getItem(currentInstituteSlug);
//       const currentInstituteType_ = sessionStorage.getItem(currentInstituteType);
//       if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['School']) {
//         this.router.navigate(['/school-workspace/' + currentInstituteSlug_ + '/profile']);
//       } else if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['College']) {
//         this.router.navigate(['/college-workspace/' + currentInstituteSlug_ + '/profile']);
//       } else if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['Coaching']) {
//         this.router.navigate(['/coaching-workspace/' + currentInstituteSlug_ + '/profile']);
//       }
//     }
//   }
// }



// @Injectable()
// export class ClassRoutingGuard implements CanLoad {
//   // Activates link if class slug exists
//   constructor(private router: Router) {}

//   canLoad(route: Route) {
//     if (sessionStorage.getItem(currentClassSlug) &&
//        sessionStorage.getItem(currentInstituteSlug) &&
//        sessionStorage.getItem(currentInstituteType) &&
//        sessionStorage.getItem(currentInstituteRole)) {
//       return true;
//     } else {
//       const currentInstituteSlug_ = sessionStorage.getItem(currentInstituteSlug)
//       const currentInstituteType_ = sessionStorage.getItem(currentInstituteType);
//       if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['School']) {
//         this.router.navigate(['/school-workspace/' + currentInstituteSlug_ + '/classes']);
//       } else if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['College']) {
//         this.router.navigate(['/college-workspace/' + currentInstituteSlug_ + '/classes']);
//       } else if (currentInstituteType_ === INSTITUTE_TYPE_REVERSE['Coaching']) {
//         this.router.navigate(['/coaching-workspace/' + currentInstituteSlug_ + '/classes']);
//       } else {
//         this.router.navigate(['/home']);
//       }
//     }
//   }
// }
