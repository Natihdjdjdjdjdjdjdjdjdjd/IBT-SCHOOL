import {
  ConflictException,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { UsersService } from '../users/users.service.js';
import { RegisterDto } from './dto/register.dto.js';
import * as argon2 from 'argon2';
import { LoginDto } from './dto/login.dto.js';
import type { User } from '../users/users.service.js';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AuthService {
  constructor(
    private readonly userService: UsersService,
    private readonly jwt: JwtService,
    private readonly config: ConfigService,
  ) {}

  async register(dto: RegisterDto) {
    const existingUser = await this.userService.findByEmail(dto.email);
    if (existingUser) {
      throw new ConflictException('User with this email already exists');
    }

    const passwordHash = await argon2.hash(dto.password);

    const newUser = await this.userService.createUser({
      email: dto.email,
      passwordHash,
    });

    return {
      id: newUser?.id,
      email: newUser?.email,
      roles: newUser?.roles,
    };
  }

  async login(dto: LoginDto) {
    const user = await this.userService.findByEmail(dto.email);

    const passwordMatches = user
      ? await argon2.verify(user.passwordHash, dto.password)
      : false;

    if (!user || !passwordMatches) {
      throw new UnauthorizedException('Invalid credentials');
    }
    return this.issueTokens(user);
  }
  private async issueTokens(user: User) {
    const accessPayload = {
      sub: user.id,
      email: user.email,
      roles: user.roles,
    };

    const [accessToken, refreshToken] = await Promise.all([
      this.jwt.signAsync(accessPayload, {
        secret: this.config.getOrThrow('JWT_ACCESS_SECRET'),
        expiresIn: '15m',
        algorithm: 'HS256',
      }),
      this.jwt.signAsync(
        { sub: user.id },
        {
          secret: this.config.getOrThrow('JWT_REFRESH_SECRET'),
          expiresIn: '7d',
          algorithm: 'HS256',
        },
      ),
    ]);

    await this.userService.setRefreshHash(
      user.id,
      await argon2.hash(refreshToken),
    );

    return {
      accessToken,
      refreshToken,
    };
  }

  async refresh(presentedToken: string) {
    try {
      const payload = await this.jwt.verifyAsync<{ sub: number }>(
        presentedToken,
        {
          secret: this.config.getOrThrow<string>('JWT_REFRESH_SECRET'),
          algorithms: ['HS256'],
        },
      );

      const user = await this.userService.findById(payload.sub);

      if (!user || !user.refreshTokenHash) {
        throw new UnauthorizedException('Invalid refresh token');
      }

      const matches = await argon2.verify(
        user.refreshTokenHash,
        presentedToken,
      );

      if (!matches) {
        throw new UnauthorizedException('Invalid refresh token');
      }

      return this.issueTokens(user);
    } catch {
      throw new UnauthorizedException('Invalid refresh token');
    }
  }

  async logout(userId: number) {
    await this.userService.setRefreshHash(userId, null);
    return { message: 'Logged out' };
  }
}
