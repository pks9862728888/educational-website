import { NativeDateAdapter, MatDateFormats } from '@angular/material/core';
import { Injectable } from "@angular/core";


@Injectable()
export class AppDateAdapter extends NativeDateAdapter {
  format(date: Date, displayFormat: Object): string {
    let day: string = date.getDate().toString();
    day = +day < 10 ? '0' + day : day;
    let month: string = (date.getMonth() + 1).toString();
    month = +month < 10 ? '0' + month : month;
    const year = date.getFullYear();
    return `${year}-${month}-${day}`;
  }
}

export const APP_DATE_FORMATS: MatDateFormats = {
  parse: {
    dateInput: { month: 'numeric', year: 'numeric', day: 'numeric' },
  },
  display: {
    dateInput: 'input',
    monthYearLabel: { year: 'numeric', month: 'numeric' },
    dateA11yLabel: { year: 'numeric', month: 'numeric', day: 'numeric'
    },
    monthYearA11yLabel: { year: 'numeric', month: 'long' },
  }
};

export function formatDate(selectedDate: string) {
  const date = new Date(selectedDate);
  let month = '' + (date.getMonth() + 1);
  let day = '' + date.getDate();
  if (month.length < 2) {
    month = '0' + month;
  }
  if (day.length < 2) {
      day = '0' + day;
  }
  return date.getFullYear() + '-' + month + '-' + day;
}

export function getUnixTimeStamp(selectedDate: string, hour: number, minute: number) {
  const date = new Date(selectedDate);
  const sheduledDate = new Date(date.getFullYear(),
                                date.getMonth(),
                                date.getDate(),
                                hour, minute);
  return +sheduledDate;
}

export function getTestSchedule(selectedDate: string, hour: number, minute: number) {
  if (!hour) {
    hour = 0;
  }
  if (!minute) {
    minute = 0;
  }
  const date = new Date(selectedDate);
  return new Date(date.getFullYear(),
                  date.getMonth(),
                  date.getDate(),
                  hour, minute);
}
