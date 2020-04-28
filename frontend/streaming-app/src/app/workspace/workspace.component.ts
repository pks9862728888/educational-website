import { Component, OnInit, DoCheck, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.css']
})
export class WorkspaceComponent implements OnInit, OnDestroy {

  // For showing sidenav toolbar
  mobileQuery: MediaQueryList;
  private mobileQueryListener: () => void;

  // For showing heading in sidenav toolbar
  userWorkspace: string;

  constructor(private router: Router,
              private route: ActivatedRoute,
              private changeDetectorRef: ChangeDetectorRef,
              private media: MediaMatcher) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this.mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this.mobileQueryListener);
    // this.mobileQuery.addEventListener('change', () => {
    //   this.mobileQueryListener();
    // });
  }

  ngOnInit(): void {
    // Rendering appropriate workspace
    if (localStorage.getItem('is_student') === JSON.stringify(true)) {
      this.userWorkspace = 'Student Workspace';
      this.router.navigate(['/workspace/student-workspace']);
    } else if (localStorage.getItem('is_teacher') === JSON.stringify(true)) {
      this.userWorkspace = 'Teacher Workspace';
      this.router.navigate(['/workspace/teacher-workspace']);
    } else if (localStorage.getItem('is_staff') === JSON.stringify(true)) {
      this.userWorkspace = 'Staff Workspace';
      this.router.navigate(['/workspace/staff-workspace']);
    } else {
      // Get the type of user and then again navigate to appropriate workspace
    }
  }

  ngOnDestroy(): void {
    this.mobileQuery.removeListener(this.mobileQueryListener);
    // this.mobileQuery.removeEventListener('change', this.mobileQueryListener);
  }

}
