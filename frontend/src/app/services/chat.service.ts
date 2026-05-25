import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface ChatRequest {
  messages: Message[];
}

export interface ChatResponse {
  reply: string;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private readonly apiUrl = 'http://localhost:8000/api/v1/chat/';

  constructor(private http: HttpClient) { }

  sendMessage(messages: Message[]): Observable<ChatResponse> {
    const body: ChatRequest = { messages };
    return this.http.post<ChatResponse>(this.apiUrl, body);
  }
}
