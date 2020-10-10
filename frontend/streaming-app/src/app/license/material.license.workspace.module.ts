import { MatExpansionModule } from '@angular/material/expansion';
import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatInputModule } from '@angular/material/input';
import { MatSliderModule } from '@angular/material/slider';


@NgModule({
    imports: [
        MatButtonModule,
        MatIconModule,
        MatCardModule,
        MatProgressSpinnerModule,
        MatExpansionModule,
        MatInputModule,
        MatSliderModule
    ],
    exports: [
        MatButtonModule,
        MatIconModule,
        MatCardModule,
        MatProgressSpinnerModule,
        MatExpansionModule,
        MatInputModule,
        MatSliderModule
    ]
})
export class LicenseMaterialWorkspaceModule { }
