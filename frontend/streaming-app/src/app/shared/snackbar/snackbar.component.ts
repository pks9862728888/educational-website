import { Component, Inject } from '@angular/core';
import { MAT_SNACK_BAR_DATA } from '@angular/material/snack-bar';

@Component({
  template: `
    <div class="snackbar-text">
      {{ this.message }}
    </div>
  `,
  styles: [`
    .snackbar-text {
      color: yellow;
      text-align: center;
    }
  `]
})
export class SnackbarComponent {
  constructor(@Inject(MAT_SNACK_BAR_DATA) public message: string) { }
}
