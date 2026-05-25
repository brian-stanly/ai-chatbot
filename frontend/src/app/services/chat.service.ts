import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface ChatRequest {
  product: string;
}

export interface ChatResponse {
  companyName: string;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private readonly apiUrl = 'http://localhost:8000/api/v1/chat';

  constructor(private http: HttpClient) { }

  sendMessage(product: string): Observable<ChatResponse> {
    const body: ChatRequest = { product };
    return this.http.post<ChatResponse>(this.apiUrl, body);
  }
}
