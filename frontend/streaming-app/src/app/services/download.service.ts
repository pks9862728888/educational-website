import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DownloadService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public async downloadFile(url: string): Promise<Blob> {
    return await this.httpClient.get<Blob>(
      url, {responseType: 'blob' as 'json'}
    ).toPromise();
  }
}
