import {Injectable} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
    providedIn: 'root'
})
export class ResearchService {
    private apiUrl = 'http://127.0.0.1:8000';

    constructor(private http:HttpClient){}


    ask(question: string): Observable<any> {
        return this.http.post(`${this.apiUrl}/ask`, {question})
    }


    askStream(question: string, onToken: (token: string) => void, onDone: () => void): void {
        fetch(`${this.apiUrl}/ask/stream`, {
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({question})
        }).then(response => {
            const reader = response.body!.getReader();
            const decoder = new TextDecoder();

            const read = () => {
                reader.read().then(({done, value}) => {
                    if (done) {onDone(); return;}
                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');
                    for (const line of lines){
                        if (line.startsWith('data: ')){
                            const data = line.slice(6);
                            if (data==='[DONE]'){onDone(); return;}
                            try {
                                const parsed = JSON.parse(data);
                                onToken(parsed.token);
                            } catch {}
                        }
                    }
                    read();
                });
            };
            read();
        })
    }
}
