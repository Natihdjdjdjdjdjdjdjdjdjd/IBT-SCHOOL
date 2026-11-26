import { Injectable } from '@nestjs/common';

export type User = {
  id: number;
  email: string;
  passwordHash: string;
  roles: string[];
  refreshTokenHash?: string | null;
};

@Injectable()
export class UsersService {
  private users: User[] = [];
  private nextId = 1;

  async findByEmail(email: string): Promise<User | undefined> {
    return this.users.find((user) => user.email === email);
  }
  async findById(id: number): Promise<User | undefined> {
    return this.users.find((user) => user.id === id);
  }

  async createUser(data: {
    email: string;
    passwordHash: string;
  }): Promise<User | undefined> {
    const newUser: User = {
      id: this.nextId++,
      email: data.email,
      passwordHash: data.passwordHash,
      roles: ['customer'],
      refreshTokenHash: null,
    };
    this.users.push(newUser);
    return newUser;
  }

  async setRefreshHash(id: number, hash: string | null): Promise<void> {
    const user = await this.findById(id);
    if (user) {
      user.refreshTokenHash = hash;
    }
  }
}
