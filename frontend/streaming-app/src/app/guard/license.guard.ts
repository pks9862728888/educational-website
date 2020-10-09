import { currentInstituteRole,
         INSTITUTE_ROLE_REVERSE,
         purchasedLicenseExists,
         paymentComplete
        } from './../../constants';
import { Router, CanActivate, RouterStateSnapshot, ActivatedRouteSnapshot } from '@angular/router';
import { Injectable } from '@angular/core';


// @Injectable()
// export class LicenseGuard implements CanActivate {
//   // Only admin can activate it

//   constructor(private router: Router) {}

//   canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
//     if (sessionStorage.getItem(currentInstituteRole) === INSTITUTE_ROLE_REVERSE.Admin) {
//       return true;
//     } else {
//       const pathName = state.url;
//       this.router.navigate([pathName.slice(0, pathName.lastIndexOf('license')) + 'profile']);
//     }
//   }
// }


// @Injectable()
// export class PurchaseLicenseGuard implements CanActivate {
//   // Only admin can activate it if there is no selected license

//   constructor( private router: Router) {}

//   canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
//     if (sessionStorage.getItem(purchasedLicenseExists) === 'false' &&
//         (!(sessionStorage.getItem(paymentComplete) === 'true')) &&
//         sessionStorage.getItem(currentInstituteRole) === INSTITUTE_ROLE_REVERSE.Admin) {
//       return true;
//     } else {
//         const pathName = state.url;
//         let path = '';
//         if (pathName.includes('purchase')) {
//           path = pathName.slice(0, pathName.lastIndexOf('purchase'));
//         } else if (pathName.includes('review')) {
//           path = pathName.slice(0, pathName.lastIndexOf('review'));
//         } else if (pathName.includes('checkout')) {
//           path = pathName.slice(0, pathName.lastIndexOf('checkout'));
//         } else {
//           path = pathName.slice(0, pathName.lastIndexOf('/') + 1);
//         }
//         this.router.navigate([path]);
//     }
//   }
// }
