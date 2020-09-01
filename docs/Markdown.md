# Markdown

参考：

[https://mermaidjs.github.io/#/](https://mermaidjs.github.io/#/)

[https://www.iminho.me/wiki/docs/mindoc/mermaid.md](https://www.iminho.me/wiki/docs/mindoc/mermaid.md)

[https://chrisniael.gitbooks.io/gitbook-documentation/content/](https://chrisniael.gitbooks.io/gitbook-documentation/content/)


引用

> 我是INFO类型引用


## 插件

Mermaid 插件

序列图
```graph
sequenceDiagram
    participant z as 张三
    participant l as 李四
    loop 日复一日
        z->>l: 吃了吗您呐？
        l-->>z: 吃了，您呢？
        activate z
        Note left of z: 想了一下
        alt 还没吃
            z-xl: 还没呢，正准备回去吃
        else 已经吃了
            z-xl: 我也吃过了，哈哈
        end
        opt 大过年的
            l-->z: 祝您新年好啊
        end
    end
```

```graph
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
```

甘特图
```graph
gantt
    title 项目开发流程
    section 项目确定
        需求分析       :a1, 2016-06-22, 3d
        可行性报告     :after a1, 5d
        概念验证       : 5d
    section 项目实施
        概要设计      :2016-07-05, 5d
        详细设计      :2016-07-08, 10d
        编码          :2016-07-15, 10d
        测试          :2016-07-22, 5d
    section 发布验收
        发布: 2d
        验收: 3d
```

第三方接口(Gravizo：http://g.gravizo.com)

免费版有水印

![Alt text](https://g.gravizo.com/svg?
    digraph G {
        main -> parse -> execute;
        main -> init;
        main -> cleanup;
        execute -> make_string;
        execute -> printf
        init -> make_string;
        main -> printf;
        execute -> compare;
    }
)


<img src='https://g.gravizo.com/svg?
@startuml;
%28*%29 --> if "Some Test" then;
  -->[true] "activity 1";
  if "" then;
    -> "activity 3" as a3;
  else;
    if "Other test" then;
      -left-> "activity 5";
    else;
      --> "activity 6";
    endif;
  endif;
else;
  ->[false] "activity 2";
endif;
a3 --> if "last test" then;
  --> "activity 7";
else;
  -> "activity 8";
endif;
@enduml 
'>


LaTex 数学符号插件


