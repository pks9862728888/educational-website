import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DownloadService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public downloadFile(url: string) {
    return this.httpClient.get(
      url, {responseType: 'blob' }
    );
  }
}
