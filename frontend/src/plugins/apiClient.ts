import {
  Middleware,
  ResponseContext,
  Configuration,
  ConfigurationParameters,
  HTTPHeaders,
  BASE_PATH,
  AuthErrorCode,
} from '@/codegen'
import router from '@/router'
import { openErrorDialog, setUserInfo, transitionLogin } from '@/plugins/utils'
import { useApiProgressStore } from '@/store/apiProgress'
import { ROUTE_NAMES } from '@/const/const'

const apiProgressStore = useApiProgressStore()

const middleware: Middleware = {
  post: async (context: ResponseContext) => {
    if (context.response.ok) {
      // ユーザー情報セット
      await setUserInfo()

      return Promise.resolve(context.response)
    }

    const status = context.response.status

    apiProgressStore.$reset()
    // 401 error
    if (status === 401) {
      const { header } = await context.response.json()
      switch (header.code) {
        case AuthErrorCode.E9011:
          router.push({ name: ROUTE_NAMES.UNAUTHORIZED })
          break
        case AuthErrorCode.E9012:
          router.push({ name: ROUTE_NAMES.UNAUTHORIZED })
          break
        case AuthErrorCode.E9013:
          openErrorDialog(header.code)
          break
        case AuthErrorCode.E9014:
          openErrorDialog(header.code)
          break
        case AuthErrorCode.E9015:
          openErrorDialog(header.code)
          break
        case AuthErrorCode.E9016:
          transitionLogin()
          break
        default:
          router.push({ name: ROUTE_NAMES.UNAUTHORIZED })
          break
      }
    }
    // 500 Error
    else if (status >= 500) {
      router.push({ name: ROUTE_NAMES.INTERNAL_SERVER_ERROR })
    } else {
      openErrorDialog()
    }
  },
  onError: async () => {
    apiProgressStore.$reset()
    // 上記で受け取れないエラーの場合は500エラー画面へ遷移
    router.push({ name: ROUTE_NAMES.INTERNAL_SERVER_ERROR })
  },
}

export class ClientConfig extends Configuration {
  constructor(configuration: ConfigurationParameters = {}) {
    super(configuration)
  }

  get basePath(): string {
    return super.basePath !== BASE_PATH
      ? super.basePath
      : import.meta.env.VITE_API_URL
  }

  get middleware(): Middleware[] {
    return super.middleware.length ? super.middleware : [middleware]
  }

  get headers(): HTTPHeaders {
    return super.headers || import.meta.env.VITE_BASIC_AUTH
      ? {
          Authorization: `Basic ${import.meta.env.VITE_BASIC_AUTH}`,
        }
      : {} // envにBASIC認証が定義されていない場合
  }

  get credentials(): RequestCredentials {
    return super.credentials || 'include'
  }
}
