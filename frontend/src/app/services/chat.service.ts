import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  history: Message[];
}

export interface ChatResponse {
  response: string;
  history: Message[];
}

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private readonly apiUrl = 'http://localhost:8000/api/chat';

  constructor(private http: HttpClient) {}

  sendMessage(message: string, history: Message[]): Observable<ChatResponse> {
    const body: ChatRequest = { message, history };
    return this.http.post<ChatResponse>(this.apiUrl, body);
  }
}
